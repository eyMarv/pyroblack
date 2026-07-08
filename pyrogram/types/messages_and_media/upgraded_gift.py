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
from typing import Dict, Optional

import pyrogram
from pyrogram import enums
from pyrogram import raw, types, utils
from ..object import Object


class UpgradedGift(Object):
    def __init__(
        self,
        *,
        client: "pyrogram.Client" = None,
        id: int,
        title: str,
        name: str,
        number: int,
        total_upgraded_count: int,
        max_upgraded_count: int,
        type: Optional["enums.GiftType"] = None,
        origin: Optional["enums.UpgradedGiftOrigin"] = None,
        received_gift_id: Optional[str] = None,
        regular_gift_id: Optional[int] = None,
        owner_id: Optional["types.Chat"] = None,
        sender: Optional["types.Chat"] = None,
        receiver: Optional["types.Chat"] = None,
        host: Optional["types.Chat"] = None,
        publisher_chat: Optional["types.Chat"] = None,
        owner_address: Optional[str] = None,
        owner_name: Optional[str] = None,
        gift_address: Optional[str] = None,
        is_name_hidden: Optional[bool] = None,
        is_saved: Optional[bool] = None,
        was_refunded: Optional[bool] = None,
        was_upgraded: Optional[bool] = None,
        export_date: Optional[datetime] = None,
        transfer_star_count: Optional[int] = None,
        next_transfer_date: Optional[datetime] = None,
        next_resale_date: Optional[datetime] = None,
        craft_date: Optional[datetime] = None,
        drop_original_details_star_count: Optional[int] = None,
        can_send_purchase_offer: Optional[bool] = None,
        minimum_offer_star_count: Optional[int] = None,
        resale_parameters: Optional["types.GiftResaleParameters"] = None,
        value_amount: Optional[int] = None,
        value_currency: Optional[str] = None,
        value_usd_amount: Optional[int] = None,
        is_premium: Optional[bool] = None,
        is_theme_available: Optional[bool] = None,
        is_burned: Optional[bool] = None,
        is_crafted: Optional[bool] = None,
        craft_probability_per_mille: Optional[int] = None,
        used_theme_chat_id: Optional[int] = None,
        _raw: "raw.types.StarGiftUnique" = None,
    ):
        super().__init__(client)
        self.id = id
        self.title = title
        self.name = name
        self.number = number
        self.total_upgraded_count = total_upgraded_count
        self.max_upgraded_count = max_upgraded_count
        self.type = type
        self.origin = origin
        self.received_gift_id = received_gift_id
        self.regular_gift_id = regular_gift_id
        self.owner_id = owner_id
        self.sender = sender
        self.receiver = receiver
        self.host = host
        self.publisher_chat = publisher_chat
        self.owner_address = owner_address
        self.owner_name = owner_name
        self.gift_address = gift_address
        self.is_name_hidden = is_name_hidden
        self.is_saved = is_saved
        self.was_refunded = was_refunded
        self.was_upgraded = was_upgraded
        self.export_date = export_date
        self.transfer_star_count = transfer_star_count
        self.next_transfer_date = next_transfer_date
        self.next_resale_date = next_resale_date
        self.craft_date = craft_date
        self.drop_original_details_star_count = drop_original_details_star_count
        self.can_send_purchase_offer = can_send_purchase_offer
        self.minimum_offer_star_count = minimum_offer_star_count
        self.resale_parameters = resale_parameters
        self.value_amount = value_amount
        self.value_currency = value_currency
        self.value_usd_amount = value_usd_amount
        self.is_premium = is_premium
        self.is_theme_available = is_theme_available
        self.is_burned = is_burned
        self.is_crafted = is_crafted
        self.craft_probability_per_mille = craft_probability_per_mille
        self.used_theme_chat_id = used_theme_chat_id
        self._raw = _raw
        self.raw = _raw

    @staticmethod
    def _parse(
        client,
        star_gift: "raw.types.StarGiftUnique",
        users: Dict[int, "raw.base.User"],
        chats: Optional[Dict[int, "raw.base.Chat"]] = None,
    ) -> "UpgradedGift":
        chats = chats or {}
        owner_id = utils.get_raw_peer_id(getattr(star_gift, 'owner_id', None))
        host_id = utils.get_raw_peer_id(getattr(star_gift, "host_id", None))
        released_by = utils.get_raw_peer_id(getattr(star_gift, "released_by", None))
        theme_peer = getattr(star_gift, "theme_peer", None)

        return UpgradedGift(
            id=star_gift.id,
            title=star_gift.title,
            name=star_gift.slug,
            number=star_gift.num,
            total_upgraded_count=star_gift.availability_issued,
            max_upgraded_count=star_gift.availability_total,
            type=enums.GiftType.UPGRADED if hasattr(enums, "GiftType") else None,
            regular_gift_id=getattr(star_gift, "gift_id", None),
            owner_id=types.Chat._parse_chat(client, users.get(owner_id) or chats.get(owner_id)) if owner_id is not None else None,
            host=types.Chat._parse_chat(client, users.get(host_id) or chats.get(host_id)) if host_id is not None else None,
            publisher_chat=types.Chat._parse_chat(client, chats.get(released_by) or users.get(released_by)) if released_by is not None else None,
            owner_address=getattr(star_gift, 'owner_address', None),
            owner_name=getattr(star_gift, 'owner_name', None),
            gift_address=getattr(star_gift, 'gift_address', None),
            can_send_purchase_offer=getattr(star_gift, "offer_min_stars", None) is not None,
            minimum_offer_star_count=getattr(star_gift, "offer_min_stars", None),
            resale_parameters=types.GiftResaleParameters._parse(
                getattr(star_gift, "resell_amount", None),
                getattr(star_gift, "resale_ton_only", False),
            ),
            value_amount=getattr(star_gift, "value_amount", None),
            value_currency=getattr(star_gift, "value_currency", None),
            value_usd_amount=getattr(star_gift, "value_usd_amount", None),
            is_premium=getattr(star_gift, "require_premium", None),
            is_theme_available=getattr(star_gift, "theme_available", None),
            is_burned=getattr(star_gift, "burned", None),
            is_crafted=getattr(star_gift, "crafted", None),
            craft_probability_per_mille=getattr(star_gift, "craft_chance_permille", None),
            used_theme_chat_id=utils.get_peer_id(theme_peer) if theme_peer is not None else None,
            _raw=star_gift,
            client=client,
        )

    @property
    def link(self) -> str:
        return f"https://t.me/nft/{self.name}"

    @property
    def owned_gift_id(self) -> Optional[str]:
        if not self.received_gift_id:
            return None

        if self.receiver and getattr(self.receiver, "type", None) != enums.ChatType.PRIVATE:
            return f"{self.receiver.id}_{self.received_gift_id}"

        return self.received_gift_id

    async def show(self) -> bool:
        if not self.owned_gift_id:
            raise ValueError("This gift doesn't have an owned_gift_id.")

        return await self._client.show_gift(
            owned_gift_id=self.owned_gift_id
        )

    async def hide(self) -> bool:
        if not self.owned_gift_id:
            raise ValueError("This gift doesn't have an owned_gift_id.")

        return await self._client.hide_gift(
            owned_gift_id=self.owned_gift_id
        )

    async def transfer(self, to_chat_id) -> Optional["types.Message"]:
        return await self._client.transfer_gift(
            owned_gift_id=self.owned_gift_id or self.link,
            new_owner_chat_id=to_chat_id,
        )

    async def wear(self) -> bool:
        return await self._client.set_emoji_status(
            emoji_status=types.EmojiStatus(gift_id=self.id)
        )

    async def buy(
        self,
        new_owner_chat_id=None,
        price: Optional["types.GiftResalePrice"] = None,
    ) -> Optional["types.Message"]:
        if new_owner_chat_id is None:
            new_owner_chat_id = "me"

        if price is None:
            if self.resale_parameters is None:
                raise ValueError("This gift doesn't expose resale parameters.")

            if self.resale_parameters.toncoin_only:
                price = types.GiftResalePriceTon(
                    toncoin_cent_count=self.resale_parameters.toncoin_cent_count
                )
            else:
                price = types.GiftResalePriceStar(
                    star_count=self.resale_parameters.star_count
                )

        return await self._client.send_resold_gift(
            gift_link=self.link,
            new_owner_chat_id=new_owner_chat_id,
            price=price,
        )

    async def send_purchase_offer(
        self,
        price: "types.GiftResalePrice",
        duration: int,
        paid_message_star_count: Optional[int] = None
    ) -> Optional["types.Message"]:
        if not self.can_send_purchase_offer:
            raise ValueError("This gift cannot be purchased via offer.")

        if not self.owner_id:
            raise ValueError("Gift owner not found.")

        return await self._client.send_gift_purchase_offer(
            owner_id=self.owner_id.id,
            gift_name=self.name,
            price=price,
            duration=duration,
            paid_message_star_count=paid_message_star_count,
        )
