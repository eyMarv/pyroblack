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

import pyrogram
from pyrogram import raw, types


class GetChatSettings:
    async def get_chat_settings(
        self: pyrogram.Client,
        chat_id: int | str,
    ) -> types.ChatSettings:
        """Get information about a chat settings.

        .. include:: /_includes/usable-by/users.rst

        Parameters
        ----------
            chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target chat.
                Unique identifier for the target chat in form of a *t.me/joinchat/* link, identifier (int) or username
                of the target channel/supergroup (in the format @username).

        Returns
        -------
            :obj:`~pyrogram.types.ChatSettings`: On success, a chat settings object is returned.

        Raises
        ------
            ValueError: In case the chat invite link points to a chat you haven't joined yet.

        Example:
            .. code-block:: python

                settings = await app.get_chat_settings("pyrogram")
                print(settings)

        """
        r = await self.invoke(
            raw.functions.messages.GetPeerSettings(
                peer=await self.resolve_peer(chat_id),
            ),
        )

        users = {i.id: i for i in r.users}
        {i.id: i for i in r.chats}

        return types.ChatSettings._parse(self, r.settings, users)
