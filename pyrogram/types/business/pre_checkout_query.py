from pyrogram import raw, types
from ..object import Object
from ..update import Update


class PreCheckoutQuery(Object, Update):
    def __init__(self, *, client=None, id: str, from_user: "types.User", currency: str, total_amount: int, invoice_payload: str, shipping_option_id: str = None, order_info: "types.OrderInfo" = None):
        super().__init__(client)
        self.id = id
        self.from_user = from_user
        self.currency = currency
        self.total_amount = total_amount
        self.invoice_payload = invoice_payload
        self.shipping_option_id = shipping_option_id
        self.order_info = order_info

    @staticmethod
    async def _parse(client, pre_checkout_query: "raw.types.UpdateBotPrecheckoutQuery", users: dict):
        try:
            payload = pre_checkout_query.payload.decode()
        except (UnicodeDecodeError, AttributeError):
            payload = pre_checkout_query.payload
        return PreCheckoutQuery(
            id=str(pre_checkout_query.query_id),
            from_user=types.User._parse(client, users[pre_checkout_query.user_id]),
            currency=pre_checkout_query.currency,
            total_amount=pre_checkout_query.total_amount,
            invoice_payload=payload,
            shipping_option_id=pre_checkout_query.shipping_option_id,
            order_info=types.OrderInfo(
                name=pre_checkout_query.info.name,
                phone_number=pre_checkout_query.info.phone,
                email=pre_checkout_query.info.email,
                shipping_address=types.ShippingAddress(
                    country_code=pre_checkout_query.info.shipping_address.country_iso2,
                    state=pre_checkout_query.info.shipping_address.state,
                    city=pre_checkout_query.info.shipping_address.city,
                    street_line1=pre_checkout_query.info.shipping_address.street_line1,
                    street_line2=pre_checkout_query.info.shipping_address.street_line2,
                    post_code=pre_checkout_query.info.shipping_address.post_code,
                ),
            ) if pre_checkout_query.info else None,
            client=client,
        )

    async def answer(self, ok: bool, error_message: str = None):
        return await self._client.answer_pre_checkout_query(
            pre_checkout_query_id=self.id,
            ok=ok,
            error_message=error_message,
        )
