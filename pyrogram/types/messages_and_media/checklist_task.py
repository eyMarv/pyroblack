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
from pyrogram.types.object import Object

from .message import Str

if TYPE_CHECKING:
    from datetime import datetime


class ChecklistTask(Object):
    """Describes a task in a checklist.

    Parameters
    ----------
        id (``int``):
            Unique identifier of the task.

        text (``str``):
            Text of the task.

        text_entities (List of :obj:`~pyrogram.types.MessageEntity`, *optional*):
            Special entities that appear in the task text.
            May contain only Bold, Italic, Underline, Strikethrough, Spoiler, CustomEmoji, Url, EmailAddress, Mention, Hashtag, Cashtag and PhoneNumber entities.

        completed_by_user (:obj:`~pyrogram.types.User`, *optional*):
            User that completed the task.
            omitted if the task wasn't completed by a user.

        completed_by_chat (:obj:`~pyrogram.types.Chat`, *optional*):
            Chat that completed the task.
            omitted if the task wasn't completed by a chat.

        completion_date (:py:obj:`~datetime.datetime`, *optional*):
            Date when the task was completed.
            None if the task isn't completed.

    """

    def __init__(
        self,
        *,
        id: int,
        text: str,
        text_entities: list[types.MessageEntity] | None = None,
        completed_by_user: types.User | None = None,
        completed_by_chat: types.Chat | None = None,
        completion_date: datetime | None = None,
    ) -> None:
        super().__init__()

        self.id = id
        self.text = text
        self.text_entities = text_entities
        self.completed_by_user = completed_by_user
        self.completed_by_chat = completed_by_chat
        self.completion_date = completion_date

    @staticmethod
    def _parse(
        client: pyrogram.Client,
        item: raw.types.TodoItem,
        completion: raw.types.TodoCompletion,
        users: dict[int, raw.base.User],
        chats: dict[int, raw.base.Chat],
    ) -> ChecklistTask:
        text_entities = [
            types.MessageEntity._parse(client, entity, users)
            for entity in item.title.entities
        ]
        text_entities = types.List(filter(lambda x: x is not None, text_entities))
        text = Str(item.title.text).init(text_entities) or None

        completed_by_peer = getattr(completion, "completed_by", None)
        completed_by_user = None
        completed_by_chat = None
        if completed_by_peer:
            completed_by_peer_id = utils.get_raw_peer_id(completed_by_peer)
            if isinstance(completed_by_peer, raw.types.PeerUser):
                completed_by_user = types.User._parse(
                    client, users.get(completed_by_peer_id)
                )
            else:
                completed_by_chat = types.Chat._parse_chat(
                    client, chats.get(completed_by_peer_id)
                )

        return ChecklistTask(
            id=item.id,
            text=text,
            text_entities=text_entities,
            completed_by_user=completed_by_user,
            completed_by_chat=completed_by_chat,
            completion_date=utils.timestamp_to_datetime(
                getattr(completion, "date", None)
            ),
        )
