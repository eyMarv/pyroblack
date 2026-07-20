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

from .message import Message
from .primitives.int import Int
from .tl_object import TLObject


class MsgContainer(TLObject):
    ID = 0x73F1F8DC

    __slots__ = ["messages"]

    QUALNAME = "MsgContainer"

    def __init__(self, messages: list[Message]) -> None:
        self.messages = messages

    @staticmethod
    def read(data: BytesIO, *args: Any) -> "MsgContainer":
        count = Int.read(data)
        return MsgContainer([Message.read(data) for _ in range(count)])

    def write(self, *args: Any) -> bytes:
        b = BytesIO()

        b.write(Int(self.ID, False))

        count = len(self.messages)
        b.write(Int(count))

        for message in self.messages:
            b.write(message.write())

        return b.getvalue()
