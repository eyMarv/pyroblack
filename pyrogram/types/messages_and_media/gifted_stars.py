import random

from pyrogram import raw, types

from ..object import Object


class GiftedStars(Object):
    """Telegram Stars were gifted to a user."""

    def __init__(
        self,
        *,
        gifter: "types.User" = None,
        receiver: "types.User" = None,
        currency: str = None,
        amount: int = None,
        cryptocurrency: str = None,
        cryptocurrency_amount: int = None,
        star_count: int = None,
        transaction_id: str = None,
        sticker: "types.Sticker" = None,
    ):
        super().__init__()

        self.gifter = gifter
        self.receiver = receiver
        self.currency = currency
        self.amount = amount
        self.cryptocurrency = cryptocurrency
        self.cryptocurrency_amount = cryptocurrency_amount
        self.star_count = star_count
        self.transaction_id = transaction_id
        self.sticker = sticker

    @staticmethod
    async def _parse(client, action, gifter=None, receiver=None) -> "GiftedStars":
        raw_stickers = await client.invoke(
            raw.functions.messages.GetStickerSet(
                stickerset=raw.types.InputStickerSetPremiumGifts(),
                hash=0
            )
        )

        return GiftedStars(
            gifter=types.User._parse(client, gifter),
            receiver=types.User._parse(client, receiver),
            currency=action.currency,
            amount=action.amount,
            cryptocurrency=getattr(action, "crypto_currency", None),
            cryptocurrency_amount=getattr(action, "crypto_amount", None),
            star_count=action.stars,
            transaction_id=getattr(action, "transaction_id", None),
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
            )
        )
