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

from pyrogram import raw, types
from pyrogram.types.object import Object


class MessageEffect(Object):
    """Contains information about an effect added to a message.

    Parameters
    ----------
        id (``int`` ``64-bit``, *optional*):
            Unique identifier of the effect.

        emoji (``str``):
            Emoji that represents the effect.

        static_icon (:obj:`~pyrogram.types.Sticker`, *optional*):
            Static icon for the effect in WEBP format; may be null if none

        effect_animation (:obj:`~pyrogram.types.Document`, *optional*):
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
        static_icon: types.Sticker | None = None,
        effect_animation: types.Document | None = None,
        select_animation: types.Document | None = None,
        is_premium: bool | None = None,
    ) -> None:
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
        effect: raw.types.AvailableEffect,
        effect_animation_document: raw.types.Document = None,
        static_icon_document: raw.types.Document = None,
        select_animation_document: raw.types.Document = None,
    ) -> MessageEffect:
        effect_animation = None
        static_icon = None
        select_animation = None

        getattr(effect, "static_icon_id", None)
        getattr(effect, "effect_animation_id", None)

        if effect_animation_document:
            effect_animation = await types.Sticker._parse(
                client,
                effect_animation_document,
                {type(i): i for i in effect_animation_document.attributes},
            )
        # TODO: FIXME!
        if static_icon_document:
            document_attributes = {type(i): i for i in static_icon_document.attributes}
            file_name = getattr(
                document_attributes.get(raw.types.DocumentAttributeFilename),
                "file_name",
                None,
            )
            static_icon = types.Document._parse(
                client,
                static_icon_document,
                file_name,
            )
        if select_animation_document:
            document_attributes = {
                type(i): i for i in select_animation_document.attributes
            }
            file_name = getattr(
                document_attributes.get(raw.types.DocumentAttributeFilename),
                "file_name",
                None,
            )
            select_animation = types.Document._parse(
                client,
                select_animation_document,
                file_name,
            )

        return MessageEffect(
            id=effect.id,
            emoji=effect.emoticon,
            static_icon=static_icon,
            effect_animation=effect_animation,  # TODO: FIXME!
            select_animation=select_animation,  # TODO: FIXME!
            is_premium=getattr(effect, "premium_required", None),
        )
