#  pyroblack - Telegram MTProto API Client Library for Python
#  Copyright (C) 2017-present Dan <https://github.com/delivrance>
#  Copyright (C) 2022-present Mayuri-Chan <https://github.com/Mayuri-Chan>
#  Copyright (C) 2024-present eyMarv <https://github.com/eyMarv>
#
#  This file is part of pyroblack.
#
#  pyroblack is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Lesser General Public License as published
#  by the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  pyroblack is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public License
#  along with pyroblack.  If not, see <http://www.gnu.org/licenses/>.

import asyncio
import bisect
import logging
import os
from time import time
from hashlib import sha1
from io import BytesIO
from typing import Optional

from pyrogram.raw.all import layer

import pyrogram
from pyrogram import raw
from pyrogram.connection import Connection
from pyrogram.crypto import mtproto
from pyrogram.errors import (
    RPCError,
    InternalServerError,
    AuthKeyDuplicated,
    FloodWait,
    FloodPremiumWait,
    ServiceUnavailable,
    BadMsgNotification,
    SecurityCheckMismatch,
    Unauthorized,
)
from pyrogram.raw.core import TLObject, MsgContainer, Int, FutureSalts
from .internals import MsgId, MsgFactory

log = logging.getLogger(__name__)


class Result:
    def __init__(self):
        self.value = None
        self.event = asyncio.Event()


class Session:
    START_TIMEOUT = 10
    WAIT_TIMEOUT = 15
    RECONN_TIMEOUT = 5
    SLEEP_THRESHOLD = 10
    MAX_RETRIES = 50
    ACKS_THRESHOLD = 10
    PING_INTERVAL = 5
    STORED_MSG_IDS_MAX_SIZE = 1000 * 2
    RECONNECT_THRESHOLD = 5
    RE_START_RANGE = (1, 2, 3, 4, 5, 6)

    TRANSPORT_ERRORS = {
        404: "auth key not found",
        429: "transport flood",
        444: "invalid DC",
    }

    def __init__(
        self,
        client: "pyrogram.Client",
        dc_id: int,
        auth_key: bytes,
        test_mode: bool,
        is_media: bool = False,
        is_cdn: bool = False,
    ):
        self.client = client
        self.dc_id = dc_id
        self.auth_key = auth_key
        self.test_mode = test_mode
        self.is_media = is_media
        self.is_cdn = is_cdn

        self.connection: Optional[Connection] = None

        self.auth_key_id = sha1(auth_key).digest()[-8:]

        self.session_id = os.urandom(8)
        self.msg_factory = MsgFactory()

        self.salt = 0

        self.pending_acks = set()

        self.results = {}

        self.stored_msg_ids = []

        self.ping_task = None
        self.ping_task_event = asyncio.Event()

        self.recv_task = None

        self.is_started = asyncio.Event()

        self.loop = asyncio.get_event_loop()

        self.instant_stop = False
        self.start_lock = asyncio.Lock()
        self.stop_lock = asyncio.Lock()
        self.restart_lock = asyncio.Lock()
        self.last_reconnect_attempt = None
        self.skip_updates_ori = client.skip_updates  # save default

    async def start(self):
        if self.instant_stop:
            return  # stop instantly

        if self.start_lock.locked():
            log.info(
                f"[pyroblack] Client [{self.client.name}] called start while already starting"
            )
            return  # don't start 2 times at once

        async with self.start_lock:
            while True:
                if self.instant_stop:
                    return  # stop instantly

                self.connection = self.client.connection_factory(
                    dc_id=self.dc_id,
                    test_mode=self.test_mode,
                    ipv6=self.client.ipv6,
                    proxy=self.client.proxy,
                    alt_port=self.client.alt_port,
                    media=self.is_media,
                    protocol_factory=self.client.protocol_factory,
                )

                try:
                    await self.connection.connect()
                    self.recv_task = self.loop.create_task(self.recv_worker())

                    await self.send(
                        raw.functions.Ping(ping_id=0), timeout=self.START_TIMEOUT
                    )

                    if not self.is_cdn:
                        await self.send(
                            raw.functions.InvokeWithLayer(
                                layer=layer,
                                query=raw.functions.InitConnection(
                                    api_id=await self.client.storage.api_id(),
                                    app_version=self.client.app_version,
                                    device_model=self.client.device_model,
                                    system_version=self.client.system_version,
                                    system_lang_code=self.client.system_lang_code,
                                    lang_code=self.client.lang_code,
                                    lang_pack=self.client.lang_pack,
                                    query=raw.functions.help.GetConfig(),
                                    params=self.client.init_params,
                                ),
                            ),
                            timeout=self.START_TIMEOUT,
                        )

                    self.ping_task = self.loop.create_task(self.ping_worker())

                    log.info("Session initialized: Layer %s", layer)
                    log.info(
                        "Device: %s - %s",
                        self.client.device_model,
                        self.client.app_version,
                    )
                    log.info(
                        "System: %s (%s)",
                        self.client.system_version,
                        self.client.lang_code,
                    )
                except AuthKeyDuplicated as e:
                    await self.stop()
                    raise e
                except (OSError, RPCError):
                    await self.stop()
                    # next try
                except Exception as e:
                    await self.stop()
                    raise e
                else:
                    break

            self.is_started.set()
            log.info("Session started")

    async def stop(self):
        if self.instant_stop:
            return  # stop doing anything instantly, force stop

        if self.stop_lock.locked():
            log.info(
                f"[pyroblack] Client [{self.client.name}] called stop while already stopping"
            )
            return  # don't stop 2 times at once

        async with self.stop_lock:
            try:
                self.instant_stop = True  # tell all funcs that we want to stop

                self.is_started.clear()
                self.stored_msg_ids.clear()

                self.ping_task_event.set()
                try:
                    if self.ping_task is not None:
                        await asyncio.wait_for(
                            self.ping_task, timeout=self.RECONN_TIMEOUT
                        )
                except TimeoutError:
                    self.ping_task.cancel()
                except Exception:
                    pass
                self.ping_task_event.clear()

                try:
                    await asyncio.wait_for(
                        self.connection.close(), timeout=self.RECONN_TIMEOUT
                    )
                except Exception:
                    pass

                try:
                    if self.recv_task:
                        await asyncio.wait_for(
                            self.recv_task, timeout=self.RECONN_TIMEOUT
                        )
                except TimeoutError:
                    self.recv_task.cancel()
                except Exception:
                    pass

                if not self.is_media and callable(self.client.disconnect_handler):
                    try:
                        await self.client.disconnect_handler(self.client)
                    except Exception as e:
                        log.error(e)

                log.info("Session stopped")
            finally:
                self.instant_stop = False  # reset

    async def restart(self, stop: bool):
        if self.instant_stop:
            return  # stop instantly

        if self.start_lock.locked():
            log.info(
                f"[pyroblack] Client [{self.client.name}] called restart while starting"
            )
            return  # don't restart while starting

        if self.restart_lock.locked():
            log.info(
                f"[pyroblack] Client [{self.client.name}] called restart while already restarting"
            )
            return  # don't restart 2 times at once

        if not self.is_started.is_set():
            log.info(
                f"[pyroblack] Client [{self.client.name}] called restart while not being already started"
            )
            return  # don't restart when supposed to be stopped

        async with self.restart_lock:
            now = time()
            if (
                self.last_reconnect_attempt
                and (now - self.last_reconnect_attempt) < self.RECONNECT_THRESHOLD
            ):
                to_wait = self.RECONNECT_THRESHOLD + int(
                    self.RECONNECT_THRESHOLD - (now - self.last_reconnect_attempt)
                )
                log.info(
                    f"[pyroblack] Client [{self.client.name}] is reconnecting too frequently, sleeping for {to_wait} seconds"
                )
                await asyncio.sleep(to_wait)

            self.last_reconnect_attempt = time()
            if stop:
                try:
                    await self.stop()
                except Exception as e:
                    log.warning(
                        f"[pyroblack] Client [{self.client.name}] failed stopping; restarting anyways, exc: %s %s",
                        type(e).__name__,
                        e,
                    )
                self.skip_updates_ori = self.client.skip_updates
                self.client.skip_updates = False  # get "missed" updates after restart

            for try_ in self.RE_START_RANGE:
                try_ += 1
                try:
                    await self.start()
                    break
                except ValueError as e:  # SQLite error
                    try:
                        await self.client.load_session()
                        log.info(
                            f"[pyroblack] Client [{self.client.name}] re-starting got SQLite error, connected to DB successfully. try %s; exc: %s %s",
                            try_,
                            type(e).__name__,
                            e,
                        )
                    except Exception as e:
                        log.warning(
                            f"[pyroblack] Client [{self.client.name}] failed re-starting SQlite DB, try %s; exc: %s %s",
                            try_,
                            type(e).__name__,
                            e,
                        )
            if stop:
                self.client.skip_updates = (
                    self.skip_updates_ori
                )  # revert to original setting
                self.skip_updates_ori = None

    async def handle_packet(self, packet):
        if self.instant_stop:
            return  # stop instantly

        try:
            data = await self.loop.run_in_executor(
                pyrogram.crypto_executor,
                mtproto.unpack,
                BytesIO(packet),
                self.session_id,
                self.auth_key,
                self.auth_key_id,
            )
        except ValueError:
            # unknown constructor
            self.loop.create_task(self.restart(stop=True))
            return

        messages = data.body.messages if isinstance(data.body, MsgContainer) else [data]

        log.debug("Received: %s", data)

        for msg in messages:
            if msg.seq_no % 2 != 0:
                if msg.msg_id in self.pending_acks:
                    continue
                else:
                    self.pending_acks.add(msg.msg_id)

            try:
                if len(self.stored_msg_ids) > Session.STORED_MSG_IDS_MAX_SIZE:
                    del self.stored_msg_ids[: Session.STORED_MSG_IDS_MAX_SIZE // 2]

                if self.stored_msg_ids:
                    if msg.msg_id < self.stored_msg_ids[0]:
                        raise SecurityCheckMismatch(
                            "The msg_id is lower than all the stored values"
                        )

                    if msg.msg_id in self.stored_msg_ids:
                        raise SecurityCheckMismatch(
                            "The msg_id is equal to any of the stored values"
                        )

                    time_diff = (msg.msg_id - MsgId()) / 2**32

                    if time_diff > 30:
                        raise SecurityCheckMismatch(
                            "The msg_id belongs to over 30 seconds in the future. "
                            "Most likely the client time has to be synchronized."
                        )

                    if time_diff < -300:
                        raise SecurityCheckMismatch(
                            "The msg_id belongs to over 300 seconds in the past. "
                            "Most likely the client time has to be synchronized."
                        )
            except SecurityCheckMismatch as e:
                log.info("Discarding packet: %s", e)
                await self.connection.close()
                return
            else:
                bisect.insort(self.stored_msg_ids, msg.msg_id)

            if isinstance(
                msg.body, (raw.types.MsgDetailedInfo, raw.types.MsgNewDetailedInfo)
            ):
                self.pending_acks.add(msg.body.answer_msg_id)
                continue

            if isinstance(msg.body, raw.types.NewSessionCreated):
                continue

            msg_id = None

            if isinstance(
                msg.body, (raw.types.BadMsgNotification, raw.types.BadServerSalt)
            ):
                msg_id = msg.body.bad_msg_id
            elif isinstance(msg.body, (FutureSalts, raw.types.RpcResult)):
                msg_id = msg.body.req_msg_id
            elif isinstance(msg.body, raw.types.Pong):
                msg_id = msg.body.msg_id
            else:
                if self.client is not None:
                    self.loop.create_task(self.client.handle_updates(msg.body))

            if msg_id in self.results:
                self.results[msg_id].value = getattr(msg.body, "result", msg.body)
                self.results[msg_id].event.set()

        if len(self.pending_acks) >= self.ACKS_THRESHOLD:
            log.debug("Sending %s acks", len(self.pending_acks))

            try:
                await self.send(
                    raw.types.MsgsAck(msg_ids=list(self.pending_acks)), False
                )
            except OSError:
                pass
            else:
                self.pending_acks.clear()

    async def ping_worker(self):
        log.info("PingTask started")

        while True:
            if self.instant_stop:
                return  # stop instantly

            try:
                await asyncio.wait_for(self.ping_task_event.wait(), self.PING_INTERVAL)
            except asyncio.TimeoutError:
                pass
            else:
                break

            try:
                await self.send(
                    raw.functions.PingDelayDisconnect(
                        ping_id=0, disconnect_delay=self.WAIT_TIMEOUT + 10
                    ),
                    False,
                )
            except OSError:
                if (not self.start_lock.locked()) and (not self.restart_lock.locked()):
                    self.loop.create_task(self.restart(stop=self.is_started.is_set()))
                break
            except RPCError:
                pass

        log.info("PingTask stopped")

    async def recv_worker(self):
        log.info("NetworkTask started")

        while True:
            if self.instant_stop:
                return  # stop instantly

            packet = await self.connection.recv()

            if packet is None or len(packet) == 4:
                if packet:
                    error_code = -Int.read(BytesIO(packet))

                    if error_code == 404:
                        raise Unauthorized(
                            "Auth key not found in the system. You must delete your session file "
                            "and log in again with your phone number or bot token."
                        )

                    log.warning(
                        "[%s] Server sent transport error: %s (%s)",
                        self.client.name,
                        error_code,
                        Session.TRANSPORT_ERRORS.get(error_code, "unknown error"),
                    )

                if (not self.start_lock.locked()) and (not self.restart_lock.locked()):
                    self.loop.create_task(self.restart(stop=self.is_started.is_set()))
                break

            self.loop.create_task(self.handle_packet(packet))

        log.info("NetworkTask stopped")

    async def send(
        self,
        data: TLObject,
        wait_response: bool = True,
        timeout: float = WAIT_TIMEOUT,
        retry: int = 0,
    ):
        if self.instant_stop:
            return  # stop instantly

        message = self.msg_factory(data)
        msg_id = message.msg_id

        if wait_response:
            self.results[msg_id] = Result()

        log.debug("Sent: %s", message)

        payload = await self.loop.run_in_executor(
            pyrogram.crypto_executor,
            mtproto.pack,
            message,
            self.salt,
            self.session_id,
            self.auth_key,
            self.auth_key_id,
        )

        try:
            await self.connection.send(payload)
        except OSError as e:
            self.results.pop(msg_id, None)
            raise e

        if wait_response:
            try:
                await asyncio.wait_for(self.results[msg_id].event.wait(), timeout)
            except asyncio.TimeoutError:
                pass

            result = self.results.pop(msg_id).value

            if result is None:
                raise TimeoutError("Request timed out")

            if isinstance(result, raw.types.RpcError):
                if isinstance(
                    data,
                    (
                        raw.functions.InvokeWithoutUpdates,
                        raw.functions.InvokeWithTakeout,
                    ),
                ):
                    data = data.query

                RPCError.raise_it(result, type(data))

            if isinstance(result, raw.types.BadMsgNotification):
                if retry > 1:
                    raise BadMsgNotification(result.error_code)

                self._handle_bad_notification()
                await self.send(data, wait_response, timeout, retry + 1)

            if isinstance(result, raw.types.BadServerSalt):
                self.salt = result.new_server_salt
                return await self.send(data, wait_response, timeout)

            return result

    def _handle_bad_notification(self):
        new_msg_id = MsgId()
        if self.stored_msg_ids[len(self.stored_msg_ids) - 1] >= new_msg_id:
            new_msg_id = self.stored_msg_ids[len(self.stored_msg_ids) - 1] + 4
            log.debug(
                "Changing msg_id old=%s new=%s",
                self.stored_msg_ids[len(self.stored_msg_ids) - 1],
                new_msg_id,
            )
        self.stored_msg_ids[len(self.stored_msg_ids) - 1] = new_msg_id

    async def invoke(
        self,
        query: TLObject,
        retries: int = MAX_RETRIES,
        timeout: float = WAIT_TIMEOUT,
        sleep_threshold: float = SLEEP_THRESHOLD,
    ):
        if isinstance(
            query, (raw.functions.InvokeWithoutUpdates, raw.functions.InvokeWithTakeout)
        ):
            inner_query = query.query
        else:
            inner_query = query

        query_name = ".".join(inner_query.QUALNAME.split(".")[1:])

        while retries > 0:
            # sleep until the restart is performed
            if self.restart_lock.locked():
                # wait until the restart is done
                await self.restart_lock.acquire()
                self.restart_lock.release()

            if self.instant_stop:
                return  # stop instantly

            if not self.is_started.is_set():
                if (
                    self.restart_lock.locked() or self.start_lock.locked()
                ):  # restarting or starting, wait
                    await self.is_started.wait()
                else:  # need to start
                    await self.start()

            try:
                return await self.send(query, timeout=timeout)
            except (FloodWait, FloodPremiumWait) as e:
                amount = e.value

                if amount > sleep_threshold >= 0:
                    raise

                log.warning(
                    '[%s] Waiting for %s seconds before continuing (required by "%s")',
                    self.client.name,
                    amount,
                    query_name,
                )

                await asyncio.sleep(amount)
            except (
                OSError,
                RuntimeError,
                InternalServerError,
                ServiceUnavailable,
                TimeoutError,
            ) as e:
                retries -= 1
                if retries == 0:
                    if callable(self.client.invoke_err_handler):
                        try:
                            await self.client.invoke_err_handler(self.client, e)
                        except Exception as ex:
                            log.error(ex)
                    raise

                if (isinstance(e, (OSError, RuntimeError)) and "handler" in str(e)) or (
                    isinstance(e, TimeoutError)
                ):
                    (log.warning if retries < 2 else log.info)(
                        '[%s] [%s] ReConnecting session requesting "%s", due to: %s',
                        self.client.name,
                        Session.MAX_RETRIES - retries,
                        query_name,
                        str(e) or repr(e),
                    )
                    self.loop.create_task(self.restart(stop=True))
                else:
                    (log.warning if retries < 2 else log.info)(
                        '[%s] [%s] Retrying "%s" due to: %s',
                        self.client.name,
                        Session.MAX_RETRIES - retries,
                        query_name,
                        str(e) or repr(e),
                    )

                await asyncio.sleep(1)
            except Exception as e:
                if callable(self.client.invoke_err_handler):
                    try:
                        await self.client.invoke_err_handler(self.client, e)
                    except Exception as ex:
                        log.error(ex)
                raise

        raise TimeoutError("Exceeded maximum number of retries")
