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

from typing import Union

from pyrogram import raw
from ..object import Object


class ForumTopicCreated(Object):
    """A service message about a new forum topic created in the chat.


    Parameters:
        id (``Integer``):
            Id of the topic

        title (``String``):
            Name of the topic.

        icon_color (``Integer``):
            Color of the topic icon in RGB format

        icon_emoji_id (``Integer``, *optional*):
            Unique identifier of the custom emoji shown as the topic icon
    """

    def __init__(
        self, *, id: int = None, title: str = None, icon_color: int = None, icon_emoji_id: int = None
    ):
        super().__init__()

        self.id = id
        self.title = title
        self.icon_color = icon_color
        self.icon_emoji_id = icon_emoji_id

        # Aliases used by the Kurigram-style chat_topics.ForumTopicCreated API
        # (and by some bots that migrated mid-release). Keep both shapes filled.
        self.name = title
        self.icon_custom_emoji_id = (
            str(icon_emoji_id) if icon_emoji_id is not None else None
        )

    @staticmethod
    def _parse(
        message_or_action: Union[
            "raw.base.Message",
            "raw.types.MessageActionTopicCreate",
        ]
    ) -> "ForumTopicCreated":
        """Parse from either a service :obj:`~pyrogram.raw.base.Message` or a bare
        :obj:`~pyrogram.raw.types.MessageActionTopicCreate`.

        Older call sites (and create_forum_topic) pass the full message so the
        topic id can be taken from ``message.id``. Message._parse historically
        (and in some 2.9.x trees) passes only the action — that path used to
        raise ``AttributeError: 'MessageActionTopicCreate' object has no
        attribute 'action'``.
        """
        topic_id = None
        action = message_or_action

        if isinstance(message_or_action, raw.types.MessageActionTopicCreate):
            action = message_or_action
        elif getattr(message_or_action, "action", None) is not None:
            # raw.base.Message (or MessageService) with .action
            topic_id = getattr(message_or_action, "id", None)
            action = message_or_action.action
        # else: already an action-like object with title/icon_color fields

        return ForumTopicCreated(
            id=topic_id,
            title=getattr(action, "title", None),
            icon_color=getattr(action, "icon_color", None),
            icon_emoji_id=getattr(action, "icon_emoji_id", None),
        )
