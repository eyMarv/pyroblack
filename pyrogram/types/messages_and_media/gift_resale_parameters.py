from typing import List, Optional

from pyrogram import raw

from ..object import Object


class GiftResaleParameters(Object):
    """Describes parameters of a unique gift available for resale."""

    def __init__(
        self,
        *,
        star_count: Optional[int] = None,
        toncoin_cent_count: Optional[int] = None,
        toncoin_only: Optional[bool] = None
    ):
        super().__init__()

        self.star_count = star_count
        self.toncoin_cent_count = toncoin_cent_count
        self.toncoin_only = toncoin_only

    @staticmethod
    def _parse(resell_amount: List["raw.base.StarsAmount"], ton_only: bool) -> Optional["GiftResaleParameters"]:
        if not resell_amount:
            return None

        star_count = None
        toncoin_cent_count = None

        for currency in resell_amount:
            if isinstance(currency, raw.types.StarsAmount):
                star_count = currency.amount
            elif isinstance(currency, raw.types.StarsTonAmount):
                toncoin_cent_count = currency.amount

        return GiftResaleParameters(
            star_count=star_count,
            toncoin_cent_count=toncoin_cent_count,
            toncoin_only=ton_only,
        )
