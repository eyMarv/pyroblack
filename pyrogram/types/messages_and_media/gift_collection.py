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
from pyrogram import raw, types

from ..object import Object


class GiftCollection(Object):
    """Describes collection of gifts.

    Parameters:
        id (``int``):
            Unique identifier of the collection.

        name (``str``):
            Name of the collection.

        gift_count (``int``):
            Total number of gifts in the collection.

        icon (:obj:`~pyrogram.types.Sticker`, *optional*):
            Icon of the collection.
    """
    def __init__(
        self, *,
        id: int,
        name: str,
        gift_count: int,
        icon: Optional["types.Sticker"] = None
    ):
        super().__init__()

        self.id = id
        self.name = name
        self.gift_count = gift_count
        self.icon = icon

    @staticmethod
    async def _parse(
        client: "pyrogram.Client",
        collection: "raw.types.StarGiftCollection"
    ) -> "GiftCollection":
        sticker = None

        if collection.icon:
            doc = collection.icon
            attributes = {type(i): i for i in doc.attributes}
            sticker = await types.Sticker._parse(client, doc, attributes)

        return GiftCollection(
            id=collection.collection_id,
            name=collection.title,
            gift_count=collection.gifts_count,
            icon=sticker
        )

