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

from pyrogram import raw, types
from ..object import Object


class AvailableEffect(Object):
    """Contains information about available effect.

    Parameters:
        id (``int``):
            Unique effect identifier.

        emoji (``str``):
            Emoji that represents the effect.

        effect_sticker_id (``int``):
            sticker identifier that represents the effect.

        sticker (:obj:`~pyrogram.types.Sticker`, *optional*):
            Sticker that represents the effect.

        is_premium (``bool``, *optional*):
            Whether the effect is available only for premium users.

        static_icon_id (``int``, *optional*):
            Static icon identifier that represents the effect.

        effect_animation_id (``int``, *optional*):
            Animation identifier that represents the effect.
    """

    def __init__(
        self,
        *,
        id: int,
        emoji: str,
        effect_sticker_id: int,
        sticker: Optional["types.Sticker"] = None,
        is_premium: Optional[bool] = None,
        static_icon_id: Optional[int] = None,
        effect_animation_id: Optional[int] = None,
    ):
        super().__init__()

        self.id = id
        self.emoji = emoji
        self.effect_sticker_id = effect_sticker_id
        self.sticker = sticker
        self.is_premium = is_premium
        self.static_icon_id = static_icon_id
        self.effect_animation_id = effect_animation_id

    @staticmethod
    async def _parse(
        client,
        effect: "raw.types.AvailableEffect",
        document: "raw.types.Document" = None,
    ) -> "AvailableEffect":
        sticker = None

        if document:
            attributes = {type(i): i for i in document.attributes}
            sticker = await types.Sticker._parse(client, document, attributes)

        return AvailableEffect(
            id=effect.id,
            emoji=effect.emoticon,
            effect_sticker_id=effect.effect_sticker_id,
            sticker=sticker,
            is_premium=getattr(effect, "premium_required", None),
            static_icon_id=getattr(effect, "static_icon_id", None),
            effect_animation_id=getattr(effect, "effect_animation_id", None),
        )
