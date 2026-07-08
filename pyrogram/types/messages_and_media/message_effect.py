#  pyroblack - Telegram MTProto API Client Library for Python
#  Copyright (C) 2017-present Dan <https://github.com/delivrance>
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

from typing import Optional

from pyrogram import raw, types
from ..object import Object


class MessageEffect(Object):
    """Contains information about an effect added to a message.

    Parameters:
        id (``int`` ``64-bit``):
            Unique identifier of the effect.

        emoji (``str``):
            Emoji that represents the effect.

        static_icon (:obj:`~pyrogram.types.Document`, *optional*):
            Static icon for the effect in WEBP format.

        effect_animation (:obj:`~pyrogram.types.Sticker`, *optional*):
            Effect animation for the effect in TGS format.

        select_animation (:obj:`~pyrogram.types.Document`, *optional*):
            Select animation for the effect in TGS format.

        is_premium (``bool``, *optional*):
            True, if Telegram Premium subscription is required to use the effect.

    """

    def __init__(
        self,
        *,
        id: int,
        emoji: str,
        static_icon: Optional["types.Document"] = None,
        effect_animation: Optional["types.Sticker"] = None,
        select_animation: Optional["types.Document"] = None,
        is_premium: Optional[bool] = None
    ):
        super().__init__()

        self.id = id
        self.emoji = emoji
        self.static_icon = static_icon
        self.effect_animation = effect_animation
        self.select_animation = select_animation
        self.is_premium = is_premium

    @staticmethod
    async def _parse(
        client,
        effect: "raw.types.AvailableEffect",
        effect_animation_document: "raw.types.Document" = None,
        static_icon_document: "raw.types.Document" = None,
        select_animation_document: "raw.types.Document" = None
    ) -> "MessageEffect":
        effect_animation = None
        static_icon = None
        select_animation = None

        if effect_animation_document:
            effect_animation = await types.Sticker._parse(
                client,
                effect_animation_document,
                {type(i): i for i in effect_animation_document.attributes}
            )
        if static_icon_document:
            document_attributes = {
                type(i): i for i in static_icon_document.attributes
            }
            file_name = getattr(document_attributes.get(raw.types.DocumentAttributeFilename, None), "file_name", None)
            static_icon = types.Document._parse(
                client,
                static_icon_document,
                file_name
            )
        if select_animation_document:
            document_attributes = {
                type(i): i for i in select_animation_document.attributes
            }
            file_name = getattr(document_attributes.get(raw.types.DocumentAttributeFilename, None), "file_name", None)
            select_animation = types.Document._parse(
                client,
                select_animation_document,
                file_name
            )

        return MessageEffect(
            id=effect.id,
            emoji=effect.emoticon,
            static_icon=static_icon,
            effect_animation=effect_animation,
            select_animation=select_animation,
            is_premium=getattr(effect, "premium_required", None)
        )
