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

import logging
from typing import TYPE_CHECKING

from .tcp import TCP

if TYPE_CHECKING:
    import asyncio

log = logging.getLogger(__name__)


class TCPAbridged(TCP):
    def __init__(
        self,
        ipv6: bool,
        proxy: dict,
        crypto_executor=None,
        loop: asyncio.AbstractEventLoop | None = None,
    ) -> None:
        super().__init__(ipv6, proxy, crypto_executor, loop)

    async def connect(self, address: tuple) -> None:
        await super().connect(address)
        await super().send(b"\xef")

    async def send(self, data: bytes, *args) -> None:
        length = len(data) // 4

        await super().send(
            (
                bytes([length])
                if length <= 126
                else b"\x7f" + length.to_bytes(3, "little")
            )
            + data,
        )

    async def recv(self, length: int = 0) -> bytes | None:
        length = await super().recv(1)

        if length is None:
            return None

        if length == b"\x7f":
            length = await super().recv(3)

            if length is None:
                return None

        return await super().recv(int.from_bytes(length, "little") * 4)
