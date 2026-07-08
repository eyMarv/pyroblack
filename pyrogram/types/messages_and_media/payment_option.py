from pyrogram import raw

from ..object import Object


class PaymentOption(Object):
    """Describes an additional payment option."""

    def __init__(
        self,
        *,
        title: str,
        url: str
    ):
        super().__init__()

        self.title = title
        self.url = url

    @staticmethod
    def _parse(option: "raw.base.PaymentFormMethod") -> "PaymentOption":
        return PaymentOption(
            title=option.title,
            url=option.url,
        )
