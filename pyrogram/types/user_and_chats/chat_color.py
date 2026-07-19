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

from pyrogram import enums, raw
from pyrogram.types.object import Object


class ChatColor(Object):
    """Accent or profile color status.

    Parameters
    ----------
        color (:obj:`~pyrogram.enums.AccentColor` | :obj:`~pyrogram.enums.ProfileColor`, *optional*):
            Color type.

        background_emoji_id (``int``, *optional*):
            Unique identifier of the custom emoji.

    """

    def __init__(
        self,
        *,
        color: enums.AccentColor | enums.ProfileColor = None,
        background_emoji_id: int | None = None,
    ) -> None:
        self.color = color
        self.background_emoji_id = background_emoji_id

    @staticmethod
    def _parse(color: raw.types.PeerColor = None) -> ChatColor | None:
        if not color:
            return None

        return ChatColor(
            color=enums.AccentColor(color.color)
            if getattr(color, "color", None)
            else None,
            background_emoji_id=getattr(color, "background_emoji_id", None),
        )

    @staticmethod
    def _parse_profile_color(color: raw.types.PeerColor = None) -> ChatColor | None:
        if not color:
            return None

        return ChatColor(
            color=enums.ProfileColor(color.color)
            if getattr(color, "color", None)
            else None,
            background_emoji_id=getattr(color, "background_emoji_id", None),
        )
