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

from typing import TYPE_CHECKING

import pyrogram
from pyrogram import raw, types, utils

if TYPE_CHECKING:
    from collections.abc import AsyncGenerator


class GetPinnedStories:
    async def get_pinned_stories(
        self: pyrogram.Client,
        chat_id: int | str,
        offset_id: int = 0,
        limit: int = 0,
    ) -> AsyncGenerator[types.Story, None]:
        """Get all pinned stories from a chat by using chat identifier.

        .. include:: /_includes/usable-by/users.rst

        Parameters
        ----------
            chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target chat.

            offset_id (``int``, *optional*):
                Offset event identifier from which to start returning results.
                By default, no offset is applied and events will be returned starting from the latest.

            limit (``int``, *optional*):
                Maximum amount of events to be returned.
                By default, all events will be returned.

        Returns
        -------
            ``Generator``: On success, a generator yielding :obj:`~pyrogram.types.Story` objects is returned.

        Example:
            .. code-block:: python

                # Get all pinned story
                async for story in app.get_pinned_stories(chat_id):
                    print(story)

        """
        current = 0
        total = abs(limit) or (1 << 31)
        limit = min(100, total)

        peer = await self.resolve_peer(chat_id)

        while True:
            r = await self.invoke(
                raw.functions.stories.GetPinnedStories(
                    peer=peer,
                    offset_id=offset_id,
                    limit=limit,
                ),
            )

            if not r.stories:
                return

            users = {i.id: i for i in r.users}
            chats = {i.id: i for i in r.chats}

            if isinstance(peer, raw.types.InputPeerChannel):
                peer_id = utils.get_raw_peer_id(peer)
                if peer_id not in r.chats:
                    channel = await self.invoke(
                        raw.functions.channels.GetChannels(id=[peer])
                    )
                    chats.update({peer_id: channel.chats[0]})

            last = r.stories[-1]
            offset_id = last.id

            for story in r.stories:
                yield await types.Story._parse(
                    self,
                    users,
                    chats,
                    None,
                    None,
                    None,
                    story,
                    peer,
                )

                current += 1

                if current >= total:
                    return
