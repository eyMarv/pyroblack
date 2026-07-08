#  pyroblack - Telegram MTProto API Client Library for Python
#  Copyright (C) 2022-present Mayuri-Chan <https://github.com/Mayuri-Chan>
#  Copyright (C) 2024-present eyMarv <https://github.com/eyMarv>
#
#  This file is part of pyroblack.
#
#  pyroblack is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Lesser General Public License as published
#  by the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  pyroblack is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public License
#  along with pyroblack.  If not, see <http://www.gnu.org/licenses/>.

from typing import Iterable, List, Union

import pyrogram
from pyrogram import raw, types


class GetDirectMessagesTopicsByID:
    async def get_direct_messages_topics_by_id(
        self: "pyrogram.Client",
        chat_id: Union[int, str],
        topic_ids: Union[int, Iterable[int]]
    ) -> Union["types.DirectMessagesTopic", List["types.DirectMessagesTopic"]]:
        """Get one or more direct message topic from a chat by using topic identifiers.

        .. include:: /_includes/usable-by/users.rst

        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target chat.

            topic_ids (``int`` | Iterable of ``int``, *optional*):
                Pass a single topic identifier or an iterable of topic ids (as integers) to get the information of the
                topic themselves.

        Returns:
            :obj:`~pyrogram.types.DirectMessagesTopic` | List of :obj:`~pyrogram.types.DirectMessagesTopic`: In case *topic_ids* was not
            a list, a single topic is returned, otherwise a list of topics is returned.

        Example:
            .. code-block:: python

                # Get one topic
                await app.get_direct_messages_topics_by_id(chat_id, 12345)

                # Get more than one topic (list of topics)
                await app.get_direct_messages_topics_by_id(chat_id, [12345, 12346])
        """
        is_iterable = not isinstance(topic_ids, int)
        ids = list(topic_ids) if is_iterable else [topic_ids]

        r = await self.invoke(
            raw.functions.messages.GetSavedDialogsByID(
                ids=[await self.resolve_peer(i) for i in ids],
                parent_peer=await self.resolve_peer(chat_id)
            )
        )

        users = {i.id: i for i in r.users}
        chats = {i.id: i for i in r.chats}

        topics = types.List()

        for i in r.dialogs:
            topics.append(types.DirectMessagesTopic._parse(client=self, topic=i, users=users, chats=chats))

        return topics if is_iterable else topics[0] if topics else None
