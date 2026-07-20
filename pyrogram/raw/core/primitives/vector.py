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

from typing import TYPE_CHECKING, Any, cast

from pyrogram.raw.core.list import List
from pyrogram.raw.core.tl_object import TLObject

from .bool import Bool, BoolFalse, BoolTrue
from .int import Int, Long

if TYPE_CHECKING:
    from io import BytesIO


class Vector(bytes, TLObject):
    ID = 0x1CB5C415

    # Method added to handle the special case when a query returns a bare Vector (of Ints);
    # i.e., RpcResult body starts with 0x1cb5c415 (Vector Id) - e.g., messages.GetMessagesViews.
    @staticmethod
    def read_bare(b: BytesIO, size: int) -> int | Any:
        if size == 4:
            # cek
            e = int.from_bytes(
                b.read(4),
                "little",
            )
            # bak
            b.seek(-4, 1)
            # cond
            if e in [
                BoolFalse.ID,
                BoolTrue.ID,
            ]:
                return Bool.read(b)
            # not
            return Int.read(b)

        if size == 8:
            return Long.read(b)

        return TLObject.read(b)

    @classmethod
    def read(cls, data: BytesIO, t: Any = None, *args: Any) -> List:
        count = Int.read(data)
        left = len(data.read())
        size = (left / count) if count else 0
        data.seek(-left, 1)

        return List(
            t.read(data) if t else Vector.read_bare(data, size) for _ in range(count)
        )

    def __new__(cls, value: list, t: Any = None) -> bytes:  # type: ignore
        return b"".join(
            [Int(cls.ID, False), Int(len(value))]
            + [cast("bytes", t(i)) if t else i.write() for i in value],
        )
