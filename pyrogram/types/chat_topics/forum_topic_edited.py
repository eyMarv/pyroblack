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

from pyrogram.types.object import Object

if TYPE_CHECKING:
    from pyrogram import raw


class ForumTopicEdited(Object):
    """This object represents a service message about an edited forum topic.

    Parameters
    ----------
        name (``str``, *optional*):
            New name of the topic, if it was edited

        icon_custom_emoji_id (``str``, *optional*):
            New identifier of the custom emoji shown as the topic icon, if it was edited; an empty string if the icon was removed

    """

    def __init__(
        self,
        *,
        name: str | None = None,
        icon_custom_emoji_id: str | None = None,
    ) -> None:
        super().__init__()

        self.name = name
        self.icon_custom_emoji_id = icon_custom_emoji_id

    @staticmethod
    def _parse(
        topic_edit_action: raw.types.MessageActionTopicEdit,
    ) -> ForumTopicEdited:
        return ForumTopicEdited(
            name=getattr(topic_edit_action, "title", None),
            icon_custom_emoji_id=getattr(topic_edit_action, "icon_emoji_id", None),
        )
