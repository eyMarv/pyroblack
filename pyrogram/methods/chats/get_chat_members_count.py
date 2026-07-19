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
from pyrogram import raw


class GetChatMembersCount:
    async def get_chat_members_count(
        self: pyrogram.Client,
        chat_id: int | str,
    ) -> int:
        """Get the number of members in a chat.

        .. include:: /_includes/usable-by/users-bots.rst

        Parameters
        ----------
            chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target chat.

        Returns
        -------
            ``int``: On success, the chat members count is returned.

        Raises
        ------
            ValueError: In case a chat id belongs to user.

        Example:
            .. code-block:: python

                count = await app.get_chat_members_count(chat_id)
                print(count)

        """
        peer = await self.resolve_peer(chat_id)

        if isinstance(peer, raw.types.InputPeerChat):
            r = await self.invoke(
                raw.functions.messages.GetChats(
                    id=[peer.chat_id],
                ),
            )

            return r.chats[0].participants_count
        if isinstance(peer, raw.types.InputPeerChannel):
            r = await self.invoke(
                raw.functions.channels.GetFullChannel(
                    channel=peer,
                ),
            )

            return r.full_chat.participants_count
        msg = f'The chat_id "{chat_id}" belongs to a user'
        raise ValueError(msg)
