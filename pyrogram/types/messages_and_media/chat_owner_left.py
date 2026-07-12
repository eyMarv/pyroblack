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

from typing import Optional

import pyrogram
from pyrogram import raw, types

from ..object import Object


class ChatOwnerLeft(Object):
    """Describes a service message about the chat owner leaving the chat.

    Parameters:
        new_owner (:obj:`~pyrogram.types.User`, *optional*):
            The user which will be the new owner of the chat if the previous owner does not return to the chat.

    """

    def __init__(self, *, new_owner: Optional["types.User"] = None):
        super().__init__()

        self.new_owner = new_owner

    @staticmethod
    def _parse(
        client: "pyrogram.Client",
        action: "raw.types.MessageActionNewCreatorPending",
        users: dict[int, "types.User"],
    ) -> "ChatOwnerLeft":
        if isinstance(action, raw.types.MessageActionNewCreatorPending):
            return ChatOwnerLeft(
                new_owner=types.User._parse(client, users.get(action.new_creator_id))
            )
