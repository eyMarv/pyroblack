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

import pyrogram
from pyrogram import raw, types
from pyrogram.types.object import Object


class ChatOwnerChanged(Object):
    """Describes a service message about an ownership change in the chat.

    Parameters
    ----------
        new_owner (:obj:`~pyrogram.types.User`):
            The new owner of the chat.

    """

    def __init__(self, *, new_owner: "types.User") -> None:
        super().__init__()

        self.new_owner = new_owner

    @staticmethod
    def _parse(
        client: "pyrogram.Client",
        action: "raw.types.MessageActionChangeCreator",
        users: dict[int, "types.User"],
    ) -> "ChatOwnerChanged":
        if isinstance(action, raw.types.MessageActionChangeCreator):
            return ChatOwnerChanged(
                new_owner=types.User._parse(client, users.get(action.new_creator_id)),
            )
        return None
