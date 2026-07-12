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

from typing import Optional

import pyrogram
from pyrogram import raw, types, utils, enums
from ..object import Object


class ForumTopicCreated(Object):
    """This object represents a service message about a new forum topic created in the chat.

    Parameters:
        name (``str``):
            Name of the topic

        icon_color  (``int``):
            Color of the topic icon in RGB format

        icon_custom_emoji_id (``str``, *optional*):
            Unique identifier of the custom emoji shown as the topic icon

        is_name_implicit (``bool``, *optional*):
            True, if the name of the topic wasn't specified explicitly by its creator and likely needs to be changed by the bot.

    """

    def __init__(
        self,
        *,
        name: str,
        icon_color: int,
        icon_custom_emoji_id: str = None,
        is_name_implicit: bool = None,
    ):
        super().__init__()

        self.name = name
        self.icon_color = icon_color
        self.icon_custom_emoji_id = icon_custom_emoji_id
        self.is_name_implicit = is_name_implicit


    @staticmethod
    def _parse(
        topic_create_action: "raw.types.MessageActionTopicCreate"
    ) -> "ForumTopicCreated":
        return ForumTopicCreated(
            name=topic_create_action.title,
            icon_color=topic_create_action.icon_color,  # TODO
            icon_custom_emoji_id=getattr(topic_create_action, "", None),
            is_name_implicit=getattr(topic_create_action, "title_missing", False),
        )
