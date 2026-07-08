from datetime import datetime

from pyrogram import raw, utils
from ..object import Object


class CollectibleItemInfo(Object):
    def __init__(self, *, purchase_date: datetime, currency: str, amount: float, cryptocurrency: str, cryptocurrency_amount: float, url: str):
        super().__init__()
        self.purchase_date = purchase_date
        self.currency = currency
        self.amount = amount
        self.cryptocurrency = cryptocurrency
        self.cryptocurrency_amount = cryptocurrency_amount
        self.url = url

    @staticmethod
    def _parse(collectible_info: "raw.types.fragment.CollectibleInfo") -> "CollectibleItemInfo":
        return CollectibleItemInfo(
            purchase_date=utils.timestamp_to_datetime(collectible_info.purchase_date),
            currency=collectible_info.currency,
            amount=collectible_info.amount,
            cryptocurrency=collectible_info.crypto_currency,
            cryptocurrency_amount=collectible_info.crypto_amount,
            url=collectible_info.url,
        )
