from typing import Optional, Union

from pyrogram import raw

from ..object import Object


class SuggestedPostPriceStar(Object):
    def __init__(self, *, star_count: int):
        super().__init__()
        self.star_count = star_count

    @staticmethod
    def _parse(post_price: "raw.types.StarsAmount") -> Optional["SuggestedPostPriceStar"]:
        if isinstance(post_price, raw.types.StarsAmount):
            return SuggestedPostPriceStar(star_count=post_price.amount)
        return None

    def write(self) -> "raw.types.StarsAmount":
        return raw.types.StarsAmount(amount=self.star_count, nanos=0)


class SuggestedPostPriceTon(Object):
    def __init__(self, *, toncoin_nano_count: int):
        super().__init__()
        self.toncoin_nano_count = toncoin_nano_count

    @staticmethod
    def _parse(post_price: "raw.types.StarsTonAmount") -> Optional["SuggestedPostPriceTon"]:
        if isinstance(post_price, raw.types.StarsTonAmount):
            return SuggestedPostPriceTon(toncoin_nano_count=post_price.amount)
        return None

    def write(self) -> "raw.types.StarsTonAmount":
        return raw.types.StarsTonAmount(amount=self.toncoin_nano_count)


class SuggestedPostPrice(Object):
    def __init__(self):
        super().__init__()

    @staticmethod
    def _parse(
        suggested_post_price: "raw.base.StarsAmount"
    ) -> Optional[Union["SuggestedPostPriceStar", "SuggestedPostPriceTon"]]:
        if isinstance(suggested_post_price, raw.types.StarsAmount):
            return SuggestedPostPriceStar._parse(suggested_post_price)
        if isinstance(suggested_post_price, raw.types.StarsTonAmount):
            return SuggestedPostPriceTon._parse(suggested_post_price)
        return None

    def write(self) -> "raw.base.StarsAmount":
        raise NotImplementedError
