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

from __future__ import annotations

import asyncio
import ipaddress
import logging
import socket
from concurrent.futures import ThreadPoolExecutor

try:
    import socks
except ImportError as e:
    e.msg = (
        "PySocks is missing and Pyrogram can't run without. "
        'Please install it using "pip3 install pysocks".'
    )
    raise

from pyrogram import utils

log = logging.getLogger(__name__)


class TCP:
    TIMEOUT = 10

    def __init__(
        self,
        ipv6: bool,
        proxy: dict,
        crypto_executor: ThreadPoolExecutor | None = None,
        loop: asyncio.AbstractEventLoop | None = None,
    ) -> None:
        self.socket = None

        self.reader = None  # type: Optional[asyncio.StreamReader]
        self.writer = None  # type: Optional[asyncio.StreamWriter]

        self.lock = asyncio.Lock()
        self.loop = loop or utils.get_event_loop()
        self.proxy = proxy

        if crypto_executor is not None:
            self.crypto_executor = crypto_executor
            self._owns_crypto_executor = False
        else:
            self.crypto_executor = ThreadPoolExecutor(
                max_workers=1,
                thread_name_prefix="CryptoWorker",
            )
            self._owns_crypto_executor = True

        if proxy:
            hostname = proxy.get("hostname")

            try:
                ip_address = ipaddress.ip_address(hostname)
            except ValueError:
                self.socket = socks.socksocket(socket.AF_INET)
            else:
                if isinstance(ip_address, ipaddress.IPv6Address):
                    self.socket = socks.socksocket(socket.AF_INET6)
                else:
                    self.socket = socks.socksocket(socket.AF_INET)

            self.socket.set_proxy(
                proxy_type=getattr(socks, proxy.get("scheme").upper()),
                addr=hostname,
                port=proxy.get("port"),
                username=proxy.get("username"),
                password=proxy.get("password"),
            )

            # PySocks still needs a blocking connect; keep the timeout for that path.
            self.socket.settimeout(TCP.TIMEOUT)
            log.info("Using proxy %s", hostname)
        else:
            # Native non-blocking socket so we can use asyncio sock_connect
            # (no temporary ThreadPoolExecutor per connect).
            self.socket = socket.socket(
                socket.AF_INET6 if ipv6 else socket.AF_INET,
            )
            self.socket.setblocking(False)

    async def connect(self, address: tuple) -> None:
        if self.proxy:
            # PySocks connect is still blocking — offload to a throwaway executor.
            with ThreadPoolExecutor(1) as executor:
                await self.loop.run_in_executor(executor, self.socket.connect, address)
        else:
            try:
                await asyncio.wait_for(
                    self.loop.sock_connect(self.socket, address),
                    TCP.TIMEOUT,
                )
            except asyncio.TimeoutError:
                msg = "Connection timed out"
                raise TimeoutError(msg)

        self.reader, self.writer = await asyncio.open_connection(sock=self.socket)

        # Socket tuning (wzgram-compatible throughput stack):
        # - TCP_NODELAY: send full MTProto parts immediately (no Nagle delay)
        # - SO_KEEPALIVE: detect dead media sessions
        # - 4 MiB SO_SNDBUF/SO_RCVBUF: raise the floor far above default
        #   (~tens of KB). Kernel may double this for bookkeeping (~8 MiB).
        #   This matches wzgram/pyrofork and keeps multi-part media sessions
        #   fed; BDP for typical VPS→DC paths is usually within this window.
        try:
            sock = self.writer.get_extra_info("socket")
            if sock is not None:
                sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
                sock.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
                sock.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 4 * 1024 * 1024)
                sock.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 4 * 1024 * 1024)
        except OSError:
            pass

    async def close(self) -> None:
        try:
            if self.writer is not None:
                self.writer.close()
                await asyncio.wait_for(self.writer.wait_closed(), TCP.TIMEOUT)
        except Exception as e:
            log.info("Close exception: %s %s", type(e).__name__, e)
        finally:
            if self._owns_crypto_executor and self.crypto_executor is not None:
                self.crypto_executor.shutdown(wait=False)
                self.crypto_executor = None

    async def send(self, data: bytes) -> None:
        async with self.lock:
            try:
                if self.writer is not None:
                    self.writer.write(data)
                    await self.writer.drain()
            except Exception as e:
                log.info("Send exception: %s %s", type(e).__name__, e)
                raise OSError(e)

    async def recv(self, length: int = 0):
        data = b""

        while len(data) < length:
            try:
                chunk = await asyncio.wait_for(
                    self.reader.read(length - len(data)),
                    TCP.TIMEOUT,
                )
            except (OSError, asyncio.TimeoutError):
                return None
            else:
                if chunk:
                    data += chunk
                else:
                    return None

        return data
