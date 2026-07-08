from datetime import datetime
from typing import Optional

from pyrogram import raw, utils

from ..object import Object


class GiftAuction(Object):
    """Describes an auction on which a gift can be purchased."""

    def __init__(self, *, id: str, gifts_per_round: int, start_date: datetime):
        super().__init__()

        self.id = id
        self.gifts_per_round = gifts_per_round
        self.start_date = start_date

    @staticmethod
    def _parse(gift: "raw.types.StarGift") -> Optional["GiftAuction"]:
        if gift.auction_slug:
            return GiftAuction(
                id=gift.auction_slug,
                gifts_per_round=gift.gifts_per_round,
                start_date=utils.timestamp_to_datetime(gift.auction_start_date),
            )

        return None
