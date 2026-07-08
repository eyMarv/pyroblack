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
from typing import Dict, Optional, Union

import pyrogram
from pyrogram import enums, raw, types, utils
from ..object import Object


class Gift(Object):
    def __init__(
        self,
        *,
        client: "pyrogram.Client" = None,
        id: int,
        sticker: "types.Sticker",
        star_count: int,
        type: Optional["enums.GiftType"] = None,
        received_gift_id: Optional[str] = None,
        title: Optional[str] = None,
        total_count: Optional[int] = None,
        remaining_count: Optional[int] = None,
        available_resale_count: Optional[int] = None,
        default_sell_star_count: int,
        convert_star_count: Optional[int] = None,
        upgrade_star_count: int,
        unique_gift_number: Optional[int] = None,
        minimum_resell_star_count: Optional[int] = None,
        unique_gift_variant_count: Optional[int] = None,
        date: Optional[datetime] = None,
        locked_until_date: Optional[datetime] = None,
        sender: Optional["types.Chat"] = None,
        receiver: Optional["types.Chat"] = None,
        publisher_chat: Optional["types.Chat"] = None,
        auction_info: Optional["types.GiftAuction"] = None,
        user_limits: Optional["types.GiftPurchaseLimit"] = None,
        overall_limits: Optional["types.GiftPurchaseLimit"] = None,
        has_colors: Optional[bool] = None,
        is_premium: Optional[bool] = None,
        is_limited_per_user: Optional[bool] = None,
        is_auction: Optional[bool] = None,
        is_for_birthday: Optional[bool] = None,
        is_name_hidden: Optional[bool] = None,
        is_saved: Optional[bool] = None,
        is_pinned: Optional[bool] = None,
        is_upgrade_separate: Optional[bool] = None,
        first_send_date: Optional[datetime] = None,
        last_send_date: Optional[datetime] = None,
        is_limited: Optional[bool] = None,
        is_sold_out: Optional[bool] = None,
        can_be_upgraded: Optional[bool] = None,
        was_refunded: Optional[bool] = None,
        was_converted: Optional[bool] = None,
        was_upgraded: Optional[bool] = None,
        export_date: Optional[datetime] = None,
        transfer_star_count: Optional[int] = None,
        next_transfer_date: Optional[datetime] = None,
        next_resale_date: Optional[datetime] = None,
        craft_date: Optional[datetime] = None,
        collection_ids: Optional[list[int]] = None,
        prepaid_upgrade_hash: Optional[str] = None,
        drop_original_details_star_count: Optional[int] = None,
        raw: Optional["raw.base.StarGift"] = None,
    ):
        super().__init__(client)
        self.id = id
        self.sticker = sticker
        self.star_count = star_count
        self.type = type
        self.received_gift_id = received_gift_id
        self.title = title
        self.total_count = total_count
        self.remaining_count = remaining_count
        self.available_resale_count = available_resale_count
        self.default_sell_star_count = default_sell_star_count
        self.convert_star_count = convert_star_count if convert_star_count is not None else default_sell_star_count
        self.upgrade_star_count = upgrade_star_count
        self.unique_gift_number = unique_gift_number
        self.minimum_resell_star_count = minimum_resell_star_count
        self.unique_gift_variant_count = unique_gift_variant_count
        self.date = date
        self.locked_until_date = locked_until_date
        self.sender = sender
        self.receiver = receiver
        self.publisher_chat = publisher_chat
        self.auction_info = auction_info
        self.user_limits = user_limits
        self.overall_limits = overall_limits
        self.has_colors = has_colors
        self.is_premium = is_premium
        self.is_limited_per_user = is_limited_per_user
        self.is_auction = is_auction
        self.is_for_birthday = is_for_birthday
        self.is_name_hidden = is_name_hidden
        self.is_saved = is_saved
        self.is_pinned = is_pinned
        self.is_upgrade_separate = is_upgrade_separate
        self.first_send_date = first_send_date
        self.last_send_date = last_send_date
        self.is_limited = is_limited
        self.is_sold_out = is_sold_out
        self.can_be_upgraded = can_be_upgraded
        self.was_refunded = was_refunded
        self.was_converted = was_converted
        self.was_upgraded = was_upgraded
        self.export_date = export_date
        self.transfer_star_count = transfer_star_count
        self.next_transfer_date = next_transfer_date
        self.next_resale_date = next_resale_date
        self.craft_date = craft_date
        self.collection_ids = collection_ids
        self.prepaid_upgrade_hash = prepaid_upgrade_hash
        self.drop_original_details_star_count = drop_original_details_star_count
        self.raw = raw

    @staticmethod
    async def _parse(
        client,
        star_gift: "raw.base.StarGift",
        receiver: Optional[Union["raw.base.User", "raw.base.Chat"]] = None,
        users: Optional[Dict[int, "raw.base.User"]] = None,
        chats: Optional[Dict[int, "raw.base.Chat"]] = None,
    ) -> Union["Gift", "types.UpgradedGift"]:
        users = users or {}
        chats = chats or {}

        if isinstance(star_gift, raw.types.StarGiftUnique):
            return types.UpgradedGift._parse(client, star_gift, users, chats)

        if isinstance(star_gift, raw.types.SavedStarGift):
            raw_from_id = utils.get_raw_peer_id(star_gift.from_id)
            parsed = await Gift._parse(
                client,
                star_gift.gift,
                receiver=receiver,
                users=users,
                chats=chats,
            )
            if parsed is None:
                return None

            if getattr(star_gift, "msg_id", None):
                parsed.received_gift_id = str(star_gift.msg_id)
            elif getattr(star_gift, "saved_id", None):
                parsed.received_gift_id = str(star_gift.saved_id)

            parsed.date = utils.timestamp_to_datetime(getattr(star_gift, "date", None)) or parsed.date
            parsed.receiver = types.Chat._parse_chat(client, receiver) if receiver is not None else getattr(parsed, "receiver", None)
            parsed.is_name_hidden = getattr(star_gift, "name_hidden", None)
            parsed.is_saved = not getattr(star_gift, "unsaved", False)
            parsed.was_refunded = getattr(star_gift, "refunded", None)
            parsed.can_be_upgraded = getattr(star_gift, "can_upgrade", None)
            parsed.is_pinned = getattr(star_gift, "pinned_to_top", None)
            parsed.is_upgrade_separate = getattr(star_gift, "upgrade_separate", None)
            parsed.sender = types.Chat._parse_chat(client, users.get(raw_from_id) or chats.get(raw_from_id)) if raw_from_id is not None else None
            parsed.convert_star_count = getattr(star_gift, "convert_stars", None) or parsed.convert_star_count
            parsed.upgrade_star_count = getattr(star_gift, "upgrade_stars", None) or parsed.upgrade_star_count
            parsed.export_date = utils.timestamp_to_datetime(getattr(star_gift, "can_export_at", None))
            parsed.transfer_star_count = getattr(star_gift, "transfer_stars", None)
            parsed.next_transfer_date = utils.timestamp_to_datetime(getattr(star_gift, "can_transfer_at", None))
            parsed.next_resale_date = utils.timestamp_to_datetime(getattr(star_gift, "can_resell_at", None))
            parsed.craft_date = utils.timestamp_to_datetime(getattr(star_gift, "can_craft_at", None))
            parsed.collection_ids = list(getattr(star_gift, "collection_id", []) or []) or None
            parsed.prepaid_upgrade_hash = getattr(star_gift, "prepaid_upgrade_hash", None)
            parsed.drop_original_details_star_count = getattr(star_gift, "drop_original_details_stars", None)
            parsed.unique_gift_number = getattr(star_gift, "gift_num", None) or parsed.unique_gift_number
            parsed.raw = star_gift
            return parsed

        if isinstance(star_gift, raw.types.MessageActionStarGift):
            parsed = await Gift._parse(client, star_gift.gift, users=users, chats=chats)
            if parsed is None:
                return None

            raw_sender_id = utils.get_raw_peer_id(star_gift.from_id)
            raw_receiver_id = utils.get_raw_peer_id(star_gift.peer)

            if getattr(star_gift, "saved_id", None):
                parsed.received_gift_id = str(star_gift.saved_id)

            parsed.is_name_hidden = getattr(star_gift, "name_hidden", None)
            parsed.is_saved = getattr(star_gift, "saved", None)
            parsed.was_converted = getattr(star_gift, "converted", None)
            parsed.was_upgraded = getattr(star_gift, "upgraded", None)
            parsed.was_refunded = getattr(star_gift, "refunded", None)
            parsed.can_be_upgraded = getattr(star_gift, "can_upgrade", None)
            parsed.is_upgrade_separate = getattr(star_gift, "upgrade_separate", None)
            parsed.convert_star_count = getattr(star_gift, "convert_stars", None) or parsed.convert_star_count
            parsed.upgrade_star_count = getattr(star_gift, "upgrade_stars", None) or parsed.upgrade_star_count
            parsed.sender = types.Chat._parse_chat(client, users.get(raw_sender_id) or chats.get(raw_sender_id)) if raw_sender_id is not None else None
            parsed.receiver = types.Chat._parse_chat(client, users.get(raw_receiver_id) or chats.get(raw_receiver_id)) if raw_receiver_id is not None else None
            parsed.prepaid_upgrade_hash = getattr(star_gift, "prepaid_upgrade_hash", None)
            parsed.unique_gift_number = getattr(star_gift, "gift_num", None) or parsed.unique_gift_number
            parsed.raw = star_gift
            return parsed

        if isinstance(star_gift, raw.types.MessageActionStarGiftUnique):
            parsed = types.UpgradedGift._parse(client, star_gift.gift, users, chats)
            raw_sender_id = utils.get_raw_peer_id(star_gift.from_id)
            raw_receiver_id = utils.get_raw_peer_id(star_gift.peer)

            if getattr(star_gift, "saved_id", None):
                parsed.received_gift_id = str(star_gift.saved_id)

            if getattr(star_gift, "from_offer", None):
                parsed.origin = enums.UpgradedGiftOrigin.OFFER
            elif getattr(star_gift, "assigned", None):
                parsed.origin = enums.UpgradedGiftOrigin.BLOCKCHAIN
            elif getattr(star_gift, "prepaid_upgrade", None):
                parsed.origin = enums.UpgradedGiftOrigin.GIFTED_UPGRADE
            elif getattr(star_gift, "resale_amount", None):
                parsed.origin = enums.UpgradedGiftOrigin.RESALE
            elif getattr(star_gift, "upgrade", None):
                parsed.origin = enums.UpgradedGiftOrigin.UPGRADE
            elif getattr(star_gift, "transferred", None):
                parsed.origin = enums.UpgradedGiftOrigin.TRANSFER
            elif getattr(star_gift, "craft", None):
                parsed.origin = enums.UpgradedGiftOrigin.CRAFT

            parsed.was_upgraded = getattr(star_gift, "upgrade", None)
            parsed.is_saved = getattr(star_gift, "saved", None)
            parsed.was_refunded = getattr(star_gift, "refunded", None)
            parsed.export_date = utils.timestamp_to_datetime(getattr(star_gift, "can_export_at", None))
            parsed.transfer_star_count = getattr(star_gift, "transfer_stars", None)
            parsed.sender = types.Chat._parse_chat(client, users.get(raw_sender_id) or chats.get(raw_sender_id)) if raw_sender_id is not None else None
            parsed.receiver = types.Chat._parse_chat(client, users.get(raw_receiver_id) or chats.get(raw_receiver_id)) if raw_receiver_id is not None else None
            parsed.next_transfer_date = utils.timestamp_to_datetime(getattr(star_gift, "can_transfer_at", None))
            parsed.next_resale_date = utils.timestamp_to_datetime(getattr(star_gift, "can_resell_at", None))
            parsed.craft_date = utils.timestamp_to_datetime(getattr(star_gift, "can_craft_at", None))
            parsed.drop_original_details_star_count = getattr(star_gift, "drop_original_details_stars", None)
            parsed.raw = star_gift
            return parsed

        doc = star_gift.sticker
        attributes = {type(i): i for i in doc.attributes}
        raw_released_by = utils.get_raw_peer_id(getattr(star_gift, "released_by", None))

        parsed = Gift(
            id=star_gift.id,
            sticker=await types.Sticker._parse(client, doc, attributes),
            star_count=star_gift.stars,
            title=getattr(star_gift, "title", None),
            default_sell_star_count=star_gift.convert_stars,
            convert_star_count=star_gift.convert_stars,
            remaining_count=getattr(star_gift, 'availability_remains', None),
            total_count=getattr(star_gift, 'availability_total', None),
            available_resale_count=getattr(star_gift, "availability_resale", None),
            first_send_date=utils.timestamp_to_datetime(getattr(star_gift, 'first_sale_date', None)),
            last_send_date=utils.timestamp_to_datetime(getattr(star_gift, 'last_sale_date', None)),
            is_limited=getattr(star_gift, 'limited', None),
            is_sold_out=getattr(star_gift, 'sold_out', None),
            upgrade_star_count=getattr(star_gift, 'upgrade_stars', 0),
            minimum_resell_star_count=getattr(star_gift, "resell_min_stars", None),
            unique_gift_variant_count=getattr(star_gift, "upgrade_variants", None),
            locked_until_date=utils.timestamp_to_datetime(getattr(star_gift, "locked_until_date", None)),
            publisher_chat=types.Chat._parse_chat(client, users.get(raw_released_by) or chats.get(raw_released_by)) if raw_released_by is not None else None,
            auction_info=types.GiftAuction._parse(star_gift),
            user_limits=types.GiftPurchaseLimit._parse(
                getattr(star_gift, "per_user_total", None),
                getattr(star_gift, "per_user_remains", None),
            ),
            overall_limits=types.GiftPurchaseLimit._parse(
                getattr(star_gift, "availability_total", None),
                getattr(star_gift, "availability_remains", None),
            ),
            has_colors=getattr(star_gift, "peer_color_available", None),
            is_premium=getattr(star_gift, "require_premium", None),
            is_limited_per_user=getattr(star_gift, "limited_per_user", None),
            is_auction=getattr(star_gift, "auction", None),
            is_for_birthday=getattr(star_gift, 'birthday', None),
            raw=star_gift,
            client=client,
        )
        parsed.type = getattr(enums, "GiftType", None).REGULAR if hasattr(enums, "GiftType") else None
        return parsed

    @property
    def owned_gift_id(self) -> Optional[str]:
        received_gift_id = getattr(self, "received_gift_id", None)
        receiver = getattr(self, "receiver", None)

        if not received_gift_id:
            return None

        if receiver and getattr(receiver, "type", None) != enums.ChatType.PRIVATE:
            return f"{receiver.id}_{received_gift_id}"

        return received_gift_id

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

    async def convert(self) -> bool:
        if not self.owned_gift_id:
            raise ValueError("This gift doesn't have an owned_gift_id.")

        return await self._client.convert_gift_to_stars(
            owned_gift_id=self.owned_gift_id
        )

    async def upgrade(
        self,
        keep_original_details: Optional[bool] = None,
        star_count: Optional[int] = None
    ) -> Optional["types.Message"]:
        if not self.owned_gift_id:
            raise ValueError("This gift doesn't have an owned_gift_id.")

        return await self._client.upgrade_gift(
            owned_gift_id=self.owned_gift_id,
            keep_original_details=keep_original_details,
            star_count=star_count,
        )

    async def send(
        self,
        chat_id: Union[int, str],
        text: Optional[str] = None,
        parse_mode: Optional["enums.ParseMode"] = None,
        entities: Optional[list["types.MessageEntity"]] = None,
        is_private: Optional[bool] = None,
        pay_for_upgrade: Optional[bool] = None,
    ) -> Optional["types.Message"]:
        return await self._client.send_gift(
            chat_id=chat_id,
            gift_id=self.id,
            text=text,
            parse_mode=parse_mode,
            entities=entities,
            is_private=is_private,
            pay_for_upgrade=pay_for_upgrade,
        )

    async def get_auction_state(self) -> "types.GiftAuctionState":
        return await self._client.get_gift_auction_state(auction_id=self.id)
