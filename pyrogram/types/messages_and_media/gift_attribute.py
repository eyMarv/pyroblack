#  Pyrogram - Telegram MTProto API Client Library for Python
#  Copyright (C) 2017-present Dan <https://github.com/delivrance>
#
#  This file is part of Pyrogram.
#
#  Pyrogram is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Lesser General Public License as published
#  by the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  Pyrogram is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public License
#  along with Pyrogram.  If not, see <http://www.gnu.org/licenses/>.

from datetime import datetime
from typing import Dict, List, Optional

from pyrogram import enums, raw, types, utils

from ..object import Object


class GiftAttribute(Object):
    def __init__(
        self,
        *,
        client=None,
        type=None,
        name: Optional[str] = None,
        backdrop_id: Optional[int] = None,
        rarity=None,
        date: Optional[datetime] = None,
        caption: Optional[str] = None,
        caption_entities: Optional[List["types.MessageEntity"]] = None,
        from_user: Optional["types.User"] = None,
        to_user: Optional["types.User"] = None,
        sticker: Optional["types.Sticker"] = None,
        center_color: Optional[int] = None,
        edge_color: Optional[int] = None,
        pattern_color: Optional[int] = None,
        text_color: Optional[int] = None,
    ):
        super().__init__(client)
        self.name = name
        self.backdrop_id = backdrop_id
        self.type = type
        self.rarity = rarity
        self.date = date
        self.caption = caption
        self.caption_entities = caption_entities
        self.from_user = from_user
        self.to_user = to_user
        self.sticker = sticker
        self.center_color = center_color
        self.edge_color = edge_color
        self.pattern_color = pattern_color
        self.text_color = text_color

    @staticmethod
    async def _parse(client, attr: "raw.base.StarGiftAttribute", users: Dict[int, "raw.base.User"], chats: Dict[int, "raw.base.Chat"]):
        caption = None
        caption_entities = None
        sticker = None
        from_user = None
        to_user = None
        rarity = None

        if hasattr(attr, "document"):
            doc = attr.document
            attributes = {type(i): i for i in doc.attributes}
            sticker = await types.Sticker._parse(client, doc, attributes)

        if isinstance(attr, raw.types.StarGiftAttributeOriginalDetails):
            caption, caption_entities = (
                utils.parse_text_with_entities(client, attr.message, users)
            ).values()

            sender_id = utils.get_raw_peer_id(attr.sender_id)
            recipient_id = utils.get_raw_peer_id(attr.recipient_id)

            from_user = types.User._parse(client, users.get(sender_id))
            to_user = types.User._parse(client, users.get(recipient_id))

        raw_rarity = getattr(attr, "rarity", None)
        if raw_rarity is not None:
            rarity = types.UpgradedGiftAttributeRarity._parse(raw_rarity)

        return GiftAttribute(
            name=getattr(attr, "name", None),
            backdrop_id=getattr(attr, "backdrop_id", None),
            type=enums.GiftAttributeType(type(attr)) if hasattr(enums, "GiftAttributeType") else type(attr),
            rarity=rarity,
            date=utils.timestamp_to_datetime(getattr(attr, "date", None)),
            caption=caption,
            caption_entities=caption_entities,
            from_user=from_user,
            to_user=to_user,
            sticker=sticker,
            center_color=getattr(attr, "center_color", None),
            edge_color=getattr(attr, "edge_color", None),
            pattern_color=getattr(attr, "pattern_color", None),
            text_color=getattr(attr, "text_color", None),
            client=client,
        )
