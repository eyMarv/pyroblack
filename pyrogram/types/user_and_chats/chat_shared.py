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

from typing import TYPE_CHECKING

from pyrogram.types.object import Object

if TYPE_CHECKING:
    from pyrogram import types


class ChatShared(Object):
    """This object contains information about a chat that was shared with the bot using a :obj:`~pyrogram.types.KeyboardButtonRequestChat` button.

    Parameters
    ----------
        request_id (``int``):
            Identifier of the request.

        chats (List of :obj:`~pyrogram.types.Chat`):
            Information about chat shared with the bot.

    """

    def __init__(
        self,
        *,
        request_id: int,
        chats: list["types.Chat"],
    ) -> None:
        super().__init__()

        self.request_id = request_id
        self.chats = chats
