from pyrogram import raw, types
from ..object import Object


class ShippingOption(Object):
    def __init__(self, id: str, title: str, prices: list["types.LabeledPrice"]):
        super().__init__()
        self.id = id
        self.title = title
        self.prices = prices

    @staticmethod
    def _parse(shipping_option: "raw.types.ShippingOption") -> "ShippingOption":
        if isinstance(shipping_option, raw.types.ShippingOption):
            return ShippingOption(
                id=shipping_option.id,
                title=shipping_option.title,
                prices=[types.LabeledPrice._parse(price) for price in shipping_option.prices],
            )

    def write(self):
        return raw.types.ShippingOption(
            id=self.id,
            title=self.title,
            prices=[price.write() for price in self.prices],
        )
