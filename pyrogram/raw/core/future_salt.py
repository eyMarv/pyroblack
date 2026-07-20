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

from io import BytesIO
from typing import Any

from .primitives.int import Int, Long
from .tl_object import TLObject


class FutureSalt(TLObject):
    ID = 0x0949D9DC

    __slots__ = ["salt", "valid_since", "valid_until"]

    QUALNAME = "FutureSalt"

    def __init__(self, valid_since: int, valid_until: int, salt: int) -> None:
        self.valid_since = valid_since
        self.valid_until = valid_until
        self.salt = salt

    @staticmethod
    def read(data: BytesIO, *args: Any) -> "FutureSalt":
        valid_since = Int.read(data)
        valid_until = Int.read(data)
        salt = Long.read(data)

        return FutureSalt(valid_since, valid_until, salt)

    def write(self, *args: Any) -> bytes:
        b = BytesIO()

        b.write(Int(self.valid_since))
        b.write(Int(self.valid_until))
        b.write(Long(self.salt))

        return b.getvalue()
