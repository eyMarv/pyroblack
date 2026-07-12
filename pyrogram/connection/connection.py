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
import logging
from typing import Optional, Type

from pyrogram.crypto.executor import get_crypto_executor
from .transport import *
from ..session.internals import DataCenter

log = logging.getLogger(__name__)


class Connection:
    MAX_RETRIES = 3

    MODES = {
        0: TCPFull,
        1: TCPAbridged,
        2: TCPIntermediate,
        3: TCPAbridgedO,
        4: TCPIntermediateO,
    }

    def __init__(
        self,
        dc_id: int,
        test_mode: bool,
        ipv6: bool,
        proxy: dict,
        media: bool = False,
        mode: int = 3,
        crypto_executor=None,
        loop: Optional[asyncio.AbstractEventLoop] = None,
    ):
        self.dc_id = dc_id
        self.test_mode = test_mode
        self.ipv6 = ipv6
        self.proxy = proxy
        self.media = media
        self.address = DataCenter(dc_id, test_mode, ipv6, media)
        self.mode = self.MODES.get(mode, TCPAbridged)
        self.crypto_executor = crypto_executor or get_crypto_executor()
        self.loop = loop

        self.protocol = None  # type: TCP

    async def connect(self):
        for i in range(Connection.MAX_RETRIES):
            self.protocol = self.mode(
                self.ipv6, self.proxy, self.crypto_executor, self.loop
            )

            try:
                log.info("Connecting...")
                await self.protocol.connect(self.address)
            except OSError as e:
                log.warning(f"Unable to connect due to network issues: {e}")
                await self.protocol.close()
                await asyncio.sleep(1)
            else:
                log.info(
                    "Connected! {} DC{}{} - IPv{} - {}".format(
                        "Test" if self.test_mode else "Production",
                        self.dc_id,
                        " (media)" if self.media else "",
                        "6" if self.ipv6 else "4",
                        self.mode.__name__,
                    )
                )
                break
        else:
            log.warning("Connection failed! Trying again...")
            raise TimeoutError

    async def close(self):
        if self.protocol is None:
            return
        # Serialize against in-flight send() so we don't tear down a writer mid-drain.
        async with self.protocol.lock:
            await self.protocol.close()
        log.info("Disconnected")

    async def send(self, data: bytes):
        try:
            await self.protocol.send(data)
        except Exception as e:
            raise OSError(e)

    async def recv(self) -> Optional[bytes]:
        return await self.protocol.recv()
