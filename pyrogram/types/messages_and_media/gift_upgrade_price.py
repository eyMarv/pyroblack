from datetime import datetime

from pyrogram import raw, utils

from ..object import Object


class GiftUpgradePrice(Object):
    """Describes a price required to pay to upgrade a gift."""

    def __init__(
        self,
        *,
        date: datetime,
        star_count: int
    ):
        super().__init__()

        self.date = date
        self.star_count = star_count

    @staticmethod
    def _parse(attr: "raw.base.StarGiftUpgradePrice") -> "GiftUpgradePrice":
        return GiftUpgradePrice(
            date=utils.timestamp_to_datetime(attr.date),
            star_count=attr.upgrade_stars,
        )
