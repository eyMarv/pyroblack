import random
from typing import Dict, List, Optional

from pyrogram import raw, types, utils

from ..object import Object


class GiftedPremium(Object):
    """Telegram Premium was gifted to the user."""

    def __init__(
        self,
        *,
        gifter: Optional["types.User"] = None,
        receiver: "types.User" = None,
        currency: Optional[str] = None,
        amount: Optional[int] = None,
        cryptocurrency: Optional[str] = None,
        cryptocurrency_amount: Optional[int] = None,
        month_count: Optional[int] = None,
        day_count: Optional[int] = None,
        sticker: Optional["types.Sticker"] = None,
        caption: Optional[str] = None,
        caption_entities: Optional[List["types.MessageEntity"]] = None,
    ):
        super().__init__()

        self.gifter = gifter
        self.receiver = receiver
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
    async def _parse(client, action, gifter, receiver, users: Dict[int, "raw.base.User"]) -> "GiftedPremium":
        raw_stickers = await client.invoke(
            raw.functions.messages.GetStickerSet(
                stickerset=raw.types.InputStickerSetPremiumGifts(),
                hash=0
            )
        )

        caption, caption_entities = (
            utils.parse_text_with_entities(client, getattr(action, "message", None), users)
        ).values()

        return GiftedPremium(
            gifter=types.User._parse(client, gifter),
            receiver=types.User._parse(client, receiver),
            currency=action.currency,
            amount=action.amount,
            cryptocurrency=getattr(action, "crypto_currency", None),
            cryptocurrency_amount=getattr(action, "crypto_amount", None),
            day_count=action.days,
            month_count=utils.get_premium_duration_month_count(action.days),
            sticker=random.choice(
                types.List(
                    [
                        await types.Sticker._parse(
                            client,
                            doc,
                            {type(item): item for item in doc.attributes}
                        )
                        for doc in raw_stickers.documents
                    ]
                )
            ),
            caption=caption,
            caption_entities=caption_entities
        )
