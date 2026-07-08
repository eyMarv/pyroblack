import random
from typing import Optional

from pyrogram import raw, types, utils

from ..object import Object


class PremiumGiftCode(Object):
    """A Telegram Premium gift code was created for the user."""

    def __init__(
        self,
        *,
        creator: Optional["types.Chat"] = None,
        text: Optional["types.FormattedText"] = None,
        is_from_giveaway: Optional[bool] = None,
        is_unclaimed: Optional[bool] = None,
        currency: Optional[str] = None,
        amount: Optional[int] = None,
        cryptocurrency: Optional[str] = None,
        cryptocurrency_amount: Optional[int] = None,
        month_count: int = None,
        day_count: int = None,
        sticker: Optional["types.Sticker"] = None,
        code: str = None
    ):
        super().__init__()

        self.creator = creator
        self.text = text
        self.is_from_giveaway = is_from_giveaway
        self.is_unclaimed = is_unclaimed
        self.currency = currency
        self.amount = amount
        self.cryptocurrency = cryptocurrency
        self.cryptocurrency_amount = cryptocurrency_amount
        self.month_count = month_count
        self.day_count = day_count
        self.sticker = sticker
        self.code = code

    @staticmethod
    async def _parse(client, giftcode, users, chats):
        raw_peer_id = utils.get_raw_peer_id(giftcode.boost_peer)
        raw_stickers = await client.invoke(
            raw.functions.messages.GetStickerSet(
                stickerset=raw.types.InputStickerSetPremiumGifts(),
                hash=0
            )
        )

        return PremiumGiftCode(
            creator=types.Chat._parse_chat(client, users.get(raw_peer_id) or chats.get(raw_peer_id)),
            text=types.FormattedText._parse(client, giftcode.message),
            is_from_giveaway=giftcode.via_giveaway,
            is_unclaimed=giftcode.unclaimed,
            currency=giftcode.currency,
            amount=giftcode.amount,
            cryptocurrency=giftcode.crypto_currency,
            cryptocurrency_amount=giftcode.crypto_amount,
            month_count=utils.get_premium_duration_month_count(giftcode.days),
            day_count=giftcode.days,
            sticker=random.choice(
                types.List(
                    [
                        await types.Sticker._parse(
                            client,
                            doc,
                            {type(item): item for item in doc.attributes}
                        ) for doc in raw_stickers.documents
                    ]
                )
            ),
            code=giftcode.slug
        )

    @property
    def link(self) -> str:
        return f"https://t.me/giftcode/{self.code}"
