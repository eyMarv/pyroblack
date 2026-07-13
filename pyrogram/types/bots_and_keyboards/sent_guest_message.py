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

from pyrogram import raw, utils

from ..object import Object


class SentGuestMessage(Object):
    """Describes an inline message sent by a guest bot.

    Parameters:
        inline_message_id (``str``):
            Identifier of the sent inline message.
    """

    def __init__(
        self,
        *,
        inline_message_id: str,
    ):
        super().__init__()

        self.inline_message_id = inline_message_id

    @staticmethod
    async def _parse(
        inline_message_id: "raw.base.InputBotInlineMessageID",
    ) -> "SentGuestMessage":
        return SentGuestMessage(inline_message_id=utils.pack_inline_message_id(inline_message_id))
