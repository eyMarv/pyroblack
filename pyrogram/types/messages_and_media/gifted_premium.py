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

from random import choice

from pyrogram import raw, types, utils
from pyrogram.types.object import Object

from .message import Str


class GiftedPremium(Object):
    """Telegram Premium was gifted to the user.

    Parameters
    ----------
        gifter_user_id (``int``):
            The identifier of a user that gifted Telegram Premium; 0 if the gift was anonymous

        currency (``str``):
            Currency for the paid amount

        amount (``int``):
            The paid amount, in the smallest units of the currency

        cryptocurrency (``str``):
            Cryptocurrency used to pay for the gift; may be empty if none

        cryptocurrency_amount (``int``):
            The paid amount, in the smallest units of the cryptocurrency; 0 if none

        month_count (``int``):
            Number of months the Telegram Premium subscription will be active.

        day_count (``int``):
            Number of days the Telegram Premium subscription will be active.

        sticker (:obj:`~pyrogram.types.Sticker`):
            A sticker to be shown in the transaction information; may be None if unknown

        caption (``str``, *optional*):
            Text message chosen by the sender.

        caption_entities (List of :obj:`~pyrogram.types.MessageEntity`, *optional*):
            Entities of the text message.

    """

    def __init__(
        self,
        *,
        gifter_user_id: int | None = None,
        currency: str | None = None,
        amount: int | None = None,
        cryptocurrency: str | None = None,
        cryptocurrency_amount: int | None = None,
        month_count: int | None = None,
        day_count: int | None = None,
        sticker: types.Sticker | None = None,
        caption: Str | None = None,
        caption_entities: list[types.MessageEntity] | None = None,
    ) -> None:
        super().__init__()

        self.gifter_user_id = gifter_user_id
        self.currency = currency
        self.amount = amount
        self.cryptocurrency = cryptocurrency
        self.cryptocurrency_amount = cryptocurrency_amount
        self.month_count = month_count
        self.day_count = day_count
        self.sticker = sticker
        self.caption = caption
        self.caption_entities = caption_entities

    @staticmethod
    async def _parse(
        client,
        gifted_premium: raw.types.MessageActionGiftPremium,
        gifter_user_id: int,
    ) -> GiftedPremium:
        sticker = None
        stickers, _ = await client._get_raw_stickers(
            raw.types.InputStickerSetPremiumGifts(),
        )
        sticker = choice(stickers)

        caption = None
        caption_entities = []
        if gifted_premium.message:
            caption_entities = [
                types.MessageEntity._parse(client, entity, {})
                for entity in gifted_premium.message.entities
            ]
            caption_entities = types.List(
                filter(lambda x: x is not None, caption_entities)
            )
            caption = Str(gifted_premium.message.text).init(caption_entities) or None

        return GiftedPremium(
            gifter_user_id=gifter_user_id,
            currency=gifted_premium.currency,
            amount=gifted_premium.amount,
            cryptocurrency=getattr(gifted_premium, "crypto_currency", None),
            cryptocurrency_amount=getattr(gifted_premium, "crypto_amount", None),
            day_count=gifted_premium.days,
            month_count=utils.get_premium_duration_month_count(gifted_premium.days),
            sticker=sticker,
            caption=caption,
            caption_entities=caption_entities or None,
        )
