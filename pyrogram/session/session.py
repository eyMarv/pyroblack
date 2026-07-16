#  Pyroblack - Telegram MTProto API Client Library for Python
#  Copyright (C) 2017-2024 Dan <https://github.com/delivrance>
#  Copyright (C) 2024-present eyMarv <https://github.com/eyMarv>
#  Maintainer: irisXDR <https://github.com/irisXDR>
#
#  This file is part of Pyroblack.
#
#  Pyroblack is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Lesser General Public License as published
#  by the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  Pyroblack is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Lesser General Public License for more details.
#
#  Pyroblack is a continuation fork of Pyrogram <https://github.com/pyrogram/pyrogram>
#
#  You should have received a copy of the GNU Lesser General Public License
#  along with Pyroblack.  If not, see <http://www.gnu.org/licenses/>.

import asyncio
import bisect
import logging
import os
from hashlib import sha1
from io import BytesIO

import pyrogram
from pyrogram import raw
from pyrogram.connection import Connection
from pyrogram.crypto import mtproto
from pyrogram.errors import (
    RPCError, InternalServerError, AuthKeyDuplicated,
    FloodWait, FloodPremiumWait,
    ServiceUnavailable, BadMsgNotification,
    SecurityCheckMismatch,
)
from pyrogram.raw.all import layer
from pyrogram.raw.core import TLObject, MsgContainer, Int, FutureSalts
from .internals import MsgId, MsgFactory

log = logging.getLogger(__name__)


class Result:
    def __init__(self):
        self.value = None
        self.event = asyncio.Event()


class Session:
    START_TIMEOUT = 2
    WAIT_TIMEOUT = 15
    SLEEP_THRESHOLD = 10
    MAX_RETRIES = 10
    ACKS_THRESHOLD = 10
    PING_INTERVAL = 5
    STORED_MSG_IDS_MAX_SIZE = 1000 * 2

    TRANSPORT_ERRORS = {
        404: "auth key not found",
        429: "transport flood",
        444: "invalid DC"
    }

    CUR_ALWD_INNR_QRYS = (
        raw.functions.InvokeWithoutUpdates,
        raw.functions.InvokeWithTakeout,
        raw.functions.InvokeWithBusinessConnection,
    )

    def __init__(
        self,
        client: "pyrogram.Client",
        dc_id: int,
        auth_key: bytes,
        test_mode: bool,
        is_media: bool = False,
        is_cdn: bool = False
    ):
        self.client = client
        self.dc_id = dc_id
        self.auth_key = auth_key
        self.test_mode = test_mode
        self.is_media = is_media
        self.is_cdn = is_cdn

        self.connection = None

        self.auth_key_id = sha1(auth_key).digest()[-8:]

        self.session_id = os.urandom(8)
        self.msg_factory = MsgFactory()

        self.salt = 0

        self.pending_acks = set()

        self.results = {}

        self.stored_msg_ids = []

        self.ping_task = None
        self.ping_task_event = asyncio.Event()

        self.network_task = None

        # Restart coordination (ported from wzgram's proven model):
        #   _restart_lock  — only one restart runs at a time
        #   _restart_done  — concurrent callers await the in-progress restart
        #                    instead of each spawning their own or timing out
        self._restart_lock = asyncio.Lock()
        self._restart_done = asyncio.Event()
        self._restart_done.set()

        self.is_started = asyncio.Event()
        self.instant_stop = False

    async def start(self):
        if self.instant_stop:
            return

        self.instant_stop = False  # reset

        while True:
            self.connection = self.client.connection_factory(
                self.dc_id,
                self.test_mode,
                self.client.ipv6,
                self.client.proxy,
                self.is_media,
                mode=getattr(self.client, "connection_mode", 1),
            )

            try:
                await self.connection.connect()

                self.network_task = self.client.loop.create_task(self.network_worker())

                await self.send(raw.functions.Ping(ping_id=0), timeout=self.START_TIMEOUT)

                if not self.is_cdn:
                    await self.send(
                        raw.functions.InvokeWithLayer(
                            layer=layer,
                            query=raw.functions.InitConnection(
                                api_id=await self.client.storage.api_id(),
                                app_version=self.client.app_version,
                                device_model=self.client.device_model,
                                system_version=self.client.system_version,
                                system_lang_code=self.client.lang_code,
                                lang_code=self.client.lang_code,
                                lang_pack="",  # "langPacks are for official apps only"
                                query=raw.functions.help.GetConfig(),
                                proxy=raw.types.InputClientProxy(
                                    address=self.client._un_docu_gnihts[0],
                                    port=self.client._un_docu_gnihts[1],
                                ) if len(self.client._un_docu_gnihts) == 3 else None,
                                params=self.client._un_docu_gnihts[2] if len(self.client._un_docu_gnihts) == 3 else (
                                    self.client.init_params if self.client.init_params else None
                                )
                            )
                        ),
                        timeout=self.START_TIMEOUT
                    )

                self.ping_task = self.client.loop.create_task(self.ping_worker())

                log.info(f"Session initialized: Layer {layer}")
                log.info(f"Device: {self.client.device_model} - {self.client.app_version}")
                log.info(f"System: {self.client.system_version} ({self.client.lang_code.upper()})")

            except AuthKeyDuplicated as e:
                await self.stop()
                raise e
            except (OSError, TimeoutError, RPCError):
                await self.stop()
                await asyncio.sleep(1)
            except Exception as e:
                await self.stop()
                raise e
            else:
                break

        self.is_started.set()

        log.info("Session started")

        if not self.is_media and callable(getattr(self.client, "connect_handler", None)):
            try:
                await self.client.connect_handler(self.client, self)
            except Exception as e:
                log.error(e, exc_info=True)

    async def stop(self):
        self.is_started.clear()

        self.stored_msg_ids.clear()

        self.ping_task_event.set()

        if self.ping_task is not None:
            await self.ping_task

        self.ping_task_event.clear()

        await self.connection.close()

        if self.network_task:
            await self.network_task

        # Wake every in-flight request so it re-checks state (and retries via
        # invoke) instead of hanging until its own timeout.
        for i in self.results.values():
            i.event.set()

        if not self.is_media and callable(self.client.disconnect_handler):
            try:
                await self.client.disconnect_handler(self.client)
            except Exception as e:
                log.error(e, exc_info=True)

        log.info("Session stopped")

    async def restart(self):
        # Coordinated restart: the first caller performs the restart; any other
        # caller that arrives while it's running simply waits for it to finish
        # rather than kicking off a competing restart or timing out on a lock.
        if self._restart_lock.locked():
            await self._restart_done.wait()
            return

        async with self._restart_lock:
            self._restart_done.clear()
            try:
                await self.stop()
                if getattr(self.client.storage, "conn", True) is None:
                    await self.client.storage.open()
                await self.start()
            finally:
                self._restart_done.set()

    async def handle_packet(self, packet):
        try:
            # Split the work across the executor boundary (ported from wzgram):
            # the crypto half (auth_key_id / msg_key / session_id verification +
            # AES-IGE) runs in the crypto executor with the GIL released, while
            # the TL deserialization runs back here on the event loop. Keeping
            # object construction off the crypto thread is the second half of the
            # throughput win — the crypto threads only do crypto.
            decrypted = await self.client.loop.run_in_executor(
                pyrogram.crypto_executor,
                mtproto.decrypt,
                packet,
                self.session_id,
                self.auth_key,
                self.auth_key_id,
            )

            data = mtproto.parse(*decrypted)
        except SecurityCheckMismatch:
            return

        messages = (
            data.body.messages
            if isinstance(data.body, MsgContainer)
            else [data]
        )

        # Call log.debug twice because calling it once by appending "data" to the previous string (i.e. f"Kind: {data}")
        # will cause "data" to be evaluated as string every time instead of only when debug is actually enabled.
        log.debug("Received:")
        log.debug(data)

        for msg in messages:
            # if msg.seq_no == 0:
            #     MsgId.set_server_time(msg.msg_id / (2 ** 32))

            if msg.seq_no % 2 != 0:
                if msg.msg_id in self.pending_acks:
                    continue
                else:
                    self.pending_acks.add(msg.msg_id)

            try:
                if len(self.stored_msg_ids) > Session.STORED_MSG_IDS_MAX_SIZE:
                    del self.stored_msg_ids[:Session.STORED_MSG_IDS_MAX_SIZE // 2]

                if self.stored_msg_ids:
                    if msg.msg_id < self.stored_msg_ids[0]:
                        raise SecurityCheckMismatch("The msg_id is lower than all the stored values")

                    if msg.msg_id in self.stored_msg_ids:
                        raise SecurityCheckMismatch("The msg_id is equal to any of the stored values")

                    time_diff = (msg.msg_id - MsgId()) / 2 ** 32

                    if time_diff > 30:
                        raise SecurityCheckMismatch("The msg_id belongs to over 30 seconds in the future. "
                                                    "Most likely the client time has to be synchronized.")

                    if time_diff < -300:
                        raise SecurityCheckMismatch("The msg_id belongs to over 300 seconds in the past. "
                                                    "Most likely the client time has to be synchronized.")
            except SecurityCheckMismatch as e:
                log.info("Discarding packet: %s", e)
                return
            else:
                bisect.insort(self.stored_msg_ids, msg.msg_id)

            if isinstance(msg.body, (raw.types.MsgDetailedInfo, raw.types.MsgNewDetailedInfo)):
                self.pending_acks.add(msg.body.answer_msg_id)
                continue

            if isinstance(msg.body, raw.types.NewSessionCreated):
                continue

            msg_id = None

            if isinstance(msg.body, (raw.types.BadMsgNotification, raw.types.BadServerSalt)):
                msg_id = msg.body.bad_msg_id
            elif isinstance(msg.body, (FutureSalts, raw.types.RpcResult)):
                msg_id = msg.body.req_msg_id
            elif isinstance(msg.body, raw.types.Pong):
                msg_id = msg.body.msg_id
            else:
                if self.client is not None:
                    self.client.loop.create_task(self.client.handle_updates(msg.body))

            if msg_id in self.results:
                self.results[msg_id].value = getattr(msg.body, "result", msg.body)
                self.results[msg_id].event.set()

        if len(self.pending_acks) >= self.ACKS_THRESHOLD:
            log.debug(f"Send {len(self.pending_acks)} acks")

            try:
                await self.send(raw.types.MsgsAck(msg_ids=list(self.pending_acks)), False)
            except (OSError, TimeoutError):
                pass
            else:
                self.pending_acks.clear()

    async def ping_worker(self):
        log.info("PingTask started")

        while True:
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
                    ), False
                )
            except (OSError, TimeoutError, RPCError):
                pass

        log.info("PingTask stopped")

    async def network_worker(self):
        log.info("NetworkTask started")

        while True:
            try:
                packet = await self.connection.recv()
            except Exception:
                if self.instant_stop:
                    break

                if self.is_started.is_set():
                    self.client.loop.create_task(self.restart())

                break

            if packet is None or len(packet) == 4:
                if packet:
                    log.warning(f'Server sent "{Int.read(BytesIO(packet))}"')

                if self.instant_stop:
                    break

                if self.is_started.is_set():
                    self.client.loop.create_task(self.restart())

                break

            self.client.loop.create_task(self.handle_packet(packet))

        log.info("NetworkTask stopped")

    async def send(
        self,
        data: TLObject,
        wait_response: bool = True,
        timeout: float = WAIT_TIMEOUT,
        retry: int = 0,
    ):
        message = self.msg_factory(data)
        msg_id = message.msg_id

        if wait_response:
            self.results[msg_id] = Result()

        # Call log.debug twice because calling it once by appending "data" to the previous string (i.e. f"Kind: {data}")
        # will cause "data" to be evaluated as string every time instead of only when debug is actually enabled.
        log.debug(f"Sent:")
        log.debug(message)

        payload = await self.client.loop.run_in_executor(
            pyrogram.crypto_executor,
            mtproto.pack,
            message,
            self.salt,
            self.session_id,
            self.auth_key,
            self.auth_key_id
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
            finally:
                result = self.results.pop(msg_id).value

            if result is None:
                raise TimeoutError
            elif isinstance(result, raw.types.RpcError):
                if isinstance(data, Session.CUR_ALWD_INNR_QRYS):
                    data = data.query

                RPCError.raise_it(result, type(data))
            elif isinstance(result, raw.types.BadMsgNotification):
                # Clock skew / msg_id race: bump our local msg_id and retry once
                # (ported from wzgram). Raising immediately used to abort healthy
                # transfers on transient BadMsg.
                if retry > 1:
                    raise BadMsgNotification(result.error_code)
                self._handle_bad_notification()
                return await self.send(data, wait_response, timeout, retry + 1)
            elif isinstance(result, raw.types.BadServerSalt):
                self.salt = result.new_server_salt
                return await self.send(data, wait_response, timeout)
            else:
                return result

    def _handle_bad_notification(self):
        new_msg_id = MsgId()
        if self.stored_msg_ids and self.stored_msg_ids[-1] >= new_msg_id:
            new_msg_id = self.stored_msg_ids[-1] + 4
            log.debug(
                "Changing msg_id old=%s new=%s",
                self.stored_msg_ids[-1],
                new_msg_id,
            )
            self.stored_msg_ids[-1] = new_msg_id

    async def invoke(
        self,
        query: TLObject,
        retries: int = MAX_RETRIES,
        timeout: float = WAIT_TIMEOUT,
        sleep_threshold: float = SLEEP_THRESHOLD
    ):
        if self.instant_stop:
            raise ConnectionError("Client was stopped")

        sleep_threshold = max(sleep_threshold, self.client.sleep_threshold)

        if isinstance(query, Session.CUR_ALWD_INNR_QRYS):
            inner_query = query.query
        else:
            inner_query = query

        query_name = ".".join(inner_query.QUALNAME.split(".")[1:])

        while retries > 0:
            if self.instant_stop:
                raise ConnectionError("Client was stopped")

            # Wait until the session is up. If a restart is in progress this
            # blocks until it finishes rather than writing into a dead socket.
            try:
                await asyncio.wait_for(self.is_started.wait(), self.WAIT_TIMEOUT)
            except asyncio.TimeoutError:
                pass

            try:
                return await self.send(query, timeout=timeout)
            except (FloodWait, FloodPremiumWait) as e:
                amount = e.value

                if amount > sleep_threshold >= 0:
                    raise

                log.warning(f'[{self.client.name}] Waiting for {amount} seconds before continuing '
                            f'(required by "{query_name}")')

                await asyncio.sleep(amount)
            except (OSError, TimeoutError, InternalServerError, ServiceUnavailable) as e:
                if self.instant_stop:
                    raise ConnectionError("Client was stopped")

                # Non-retryable server-side conditions: surface immediately.
                if (
                    isinstance(e, InternalServerError) and
                    getattr(e, "code", 0) == 500 and
                    (getattr(e, "ID", None) or getattr(e, "NAME", None)) in [
                        "HISTORY_GET_FAILED",
                        "PERSISTENT_TIMESTAMP_OUTDATED",
                    ]
                ):
                    if callable(self.client.invoke_err_handler):
                        try:
                            await self.client.invoke_err_handler(self.client, e)
                        except Exception:
                            pass
                    raise e from None

                retries -= 1
                if retries == 0:
                    if callable(self.client.invoke_err_handler):
                        try:
                            await self.client.invoke_err_handler(self.client, e)
                        except Exception:
                            pass
                    raise

                (log.warning if retries < 2 else log.info)(
                    f'[{Session.MAX_RETRIES - retries}] Retrying "{query_name}" due to {str(e) or repr(e)}')

                if callable(self.client.invoke_err_handler):
                    try:
                        await self.client.invoke_err_handler(self.client, e)
                    except Exception:
                        pass

                # Rebuild the connection for genuine transport failures; for
                # transient server errors just back off briefly. This is the
                # crucial recovery path — a dead media socket is restarted here
                # and the request retried on the fresh connection.
                if isinstance(e, (OSError, TimeoutError)):
                    await self.restart()
                else:
                    await asyncio.sleep(1)

        raise TimeoutError("Exceeded maximum number of retries")
