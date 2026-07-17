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
        message_or_action: "raw.types.MessageActionTopicCreate"
    ) -> "ForumTopicCreated":
        # Accept bare MessageActionTopicCreate or a service Message that wraps it.
        action = message_or_action
        if getattr(message_or_action, "action", None) is not None:
            action = message_or_action.action

        icon_emoji_id = getattr(action, "icon_emoji_id", None)
        return ForumTopicCreated(
            name=getattr(action, "title", None),
            icon_color=getattr(action, "icon_color", None),
            icon_custom_emoji_id=str(icon_emoji_id) if icon_emoji_id is not None else None,
            is_name_implicit=bool(getattr(action, "title_missing", False)),
        )
