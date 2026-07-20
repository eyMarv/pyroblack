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


class ToggleForumTopicIsPinned:
    async def toggle_forum_topic_is_pinned(
        self: pyrogram.Client,
        chat_id: int | str,
        message_thread_id: int,
        is_pinned: bool,
    ) -> bool:
        """Changes the pinned state of a forum topic; requires can_manage_topics right in the supergroup. There can be up to ``pinned_forum_topic_count_max`` pinned forum topics.

        .. include:: /_includes/usable-by/users.rst

        Parameters
        ----------
            chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target chat.

            message_thread_id (``int``):
                Unique identifier for the target message thread of the forum topic.

            is_pinned (``bool``):
                Pass True to pin the topic; pass False to unpin it.

        Returns
        -------
            ``bool``: On success, True is returned.

        Raises
        ------
            :obj:`~pyrogram.errors.RPCError`: In case of a Telegram RPC error.

        Example:
            .. code-block:: python

                await app.toggle_forum_topic_is_pinned(chat_id, topic_id, True)

        """
        await self.invoke(
            raw.functions.messages.UpdatePinnedForumTopic(
                peer=await self.resolve_peer(chat_id),
                topic_id=message_thread_id,
                pinned=is_pinned,
            ),
        )
        # TODO
        return True
