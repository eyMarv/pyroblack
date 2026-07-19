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


class GetSendAsChats:
    async def get_send_as_chats(
        self: pyrogram.Client,
        chat_id: int | str,
        for_paid_reactions: bool | None = None,
        for_live_stories: bool | None = None,
    ) -> list[types.Chat]:
        """Get the list of "send_as" chats available.

        .. include:: /_includes/usable-by/users.rst

        Parameters
        ----------
            chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target chat.

            for_paid_reactions (``bool``, *optional*):
                Pass True to get the list of available send_as chats for paid reactions.

            for_live_stories (``bool``, *optional*):
                Pass True to get the list of available send_as chats for viewing live stories.

        Returns
        -------
            List of :obj:`~pyrogram.types.Chat`: The list of chats.

        Example:
            .. code-block:: python

                chats = await app.get_send_as_chats(chat_id)
                print(chats)

        """
        r = await self.invoke(
            raw.functions.channels.GetSendAs(
                peer=await self.resolve_peer(chat_id),
                for_paid_reactions=for_paid_reactions,
                for_live_stories=for_live_stories,
            ),
        )

        users = {u.id: u for u in r.users}
        chats = {c.id: c for c in r.chats}

        send_as_chats = types.List()

        for p in r.peers:
            # TODO
            if isinstance(p.peer, raw.types.PeerUser):
                send_as_chats.append(
                    types.Chat._parse_chat(self, users[p.peer.user_id])
                )
            else:
                send_as_chats.append(
                    types.Chat._parse_chat(self, chats[p.peer.channel_id])
                )

        return send_as_chats
