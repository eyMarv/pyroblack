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

import logging
from typing import TYPE_CHECKING

import pyrogram
from pyrogram import raw, types

if TYPE_CHECKING:
    from collections.abc import Iterable

log = logging.getLogger(__name__)


class GetForumTopicsByID:
    async def get_forum_topics_by_id(
        self: pyrogram.Client,
        chat_id: int | str,
        topic_ids: int | Iterable[int],
    ) -> types.ForumTopic | list[types.ForumTopic]:
        """Get one or more topic from a chat by using topic identifiers.

        .. include:: /_includes/usable-by/users.rst

        Parameters
        ----------
            chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target chat.
                You can also use chat public link in form of *t.me/<username>* (str).

            topic_ids (``int`` | Iterable of ``int``, *optional*):
                Pass a single topic identifier or an iterable of topic ids (as integers) to get the information of the
                topic themselves.

        Returns
        -------
            :obj:`~pyrogram.types.ForumTopic` | List of :obj:`~pyrogram.types.ForumTopic`: In case *topic_ids* was not
            a list, a single topic is returned, otherwise a list of topics is returned.

        Example:
            .. code-block:: python

                # Get one topic
                await app.get_forum_topics_by_id(chat_id, 12345)

                # Get more than one topic (list of topics)
                await app.get_forum_topics_by_id(chat_id, [12345, 12346])

        Raises
        ------
            ValueError: In case of invalid arguments.

        """
        ids, _ = (topic_ids, int) if topic_ids else (None, None)

        if ids is None:
            msg = "No argument supplied. Either pass topic_ids"
            raise ValueError(msg)

        peer = await self.resolve_peer(chat_id)

        is_iterable = not isinstance(ids, int)
        ids = list(ids) if is_iterable else [ids]
        ids = list(ids)

        rpc = raw.functions.channels.GetForumTopicsByID(channel=peer, topics=ids)

        r = await self.invoke(rpc, sleep_threshold=-1)

        if is_iterable:
            topic_list = []
            for topic in r.topics:
                topic_list.append(types.ForumTopic._parse(topic))
            topics = types.List(topic_list)
        else:
            topics = types.ForumTopic._parse(r.topics[0])

        return topics
