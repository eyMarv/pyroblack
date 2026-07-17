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

from pyrogram import raw
from ..object import Object


class ForumTopicEdited(Object):
    """A service message about a forum topic renamed in the chat.


    Parameters:
        title (``String``):
            Name of the topic.

        icon_color (``Integer``):
            Color of the topic icon in RGB format

        icon_custom_emoji_id (``String``, *optional*):
            Unique identifier of the custom emoji shown as the topic icon
    """

    def __init__(
        self, *, title: str = None, icon_color: int = None, icon_emoji_id: str = None
    ):
        super().__init__()

        self.title = title
        self.icon_color = icon_color
        self.icon_emoji_id = icon_emoji_id

    @staticmethod
    def _parse(action: "raw.types.MessageActionTopicEdit") -> "ForumTopicEdited":
        # Accept bare action or a service Message wrapping it.
        if getattr(action, "action", None) is not None:
            action = action.action
        return ForumTopicEdited(
            title=getattr(action, "title", None),
            icon_color=getattr(action, "icon_color", None),
            icon_emoji_id=getattr(action, "icon_emoji_id", None),
        )
