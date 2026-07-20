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


class GetSuitableDiscussionChats:
    async def get_suitable_discussion_chats(
        self: "pyrogram.Client",
    ) -> list["types.Chat"]:
        """Return a list of basic group and supergroup chats, which can be used as a discussion group for a channel.

        Returned basic group chats must be first upgraded to supergroups before they can be set as a discussion group.

        .. include:: /_includes/usable-by/users.rst

        Returns:
            List of :obj:`~pyrogram.types.Chat`: List of suitable discussion chats.

        Example:
            .. code-block:: python

                chats = await app.get_suitable_discussion_chats()

        """
        r = await self.invoke(
            raw.functions.channels.GetGroupsForDiscussion(),
        )

        return types.List([types.Chat._parse_chat(self, i) for i in r.chats])
