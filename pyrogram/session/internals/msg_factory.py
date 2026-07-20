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

from pyrogram.raw.core import Message, MsgContainer, TLObject
from pyrogram.raw.functions import Ping
from pyrogram.raw.types import HttpWait, MsgsAck

from .msg_id import MsgId
from .seq_no import SeqNo

not_content_related = (Ping, HttpWait, MsgsAck, MsgContainer)


class MsgFactory:
    def __init__(self) -> None:
        self.seq_no = SeqNo()

    def __call__(self, body: TLObject) -> Message:
        return Message(
            body,
            MsgId(),
            self.seq_no(not isinstance(body, not_content_related)),
            len(body),
        )
