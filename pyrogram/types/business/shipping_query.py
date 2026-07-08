from typing import Union

import pyrogram
from pyrogram import raw, types
from ..object import Object
from ..update import Update


class ShippingQuery(Object, Update):
    def __init__(self, *, client: "pyrogram.Client" = None, id: str, from_user: "types.User", invoice_payload: str, shipping_address: "types.ShippingAddress" = None):
        super().__init__(client)
        self.id = id
        self.from_user = from_user
        self.invoice_payload = invoice_payload
        self.shipping_address = shipping_address

    @staticmethod
    async def _parse(client: "pyrogram.Client", shipping_query: "raw.types.updateBotShippingQuery", users: dict) -> "ShippingQuery":
        try:
            payload = shipping_query.payload.decode()
        except (UnicodeDecodeError, AttributeError):
            payload = shipping_query.payload
        return ShippingQuery(
            id=str(shipping_query.query_id),
            from_user=types.User._parse(client, users[shipping_query.user_id]),
            invoice_payload=payload,
            shipping_address=types.ShippingAddress(
                country_code=shipping_query.shipping_address.country_iso2,
                state=shipping_query.shipping_address.state,
                city=shipping_query.shipping_address.city,
                street_line1=shipping_query.shipping_address.street_line1,
                street_line2=shipping_query.shipping_address.street_line2,
                post_code=shipping_query.shipping_address.post_code,
            ),
            client=client,
        )

    async def answer(self, ok: bool, shipping_options: "types.ShippingOptions" = None, error_message: str = None):
        return await self._client.answer_shipping_query(
            shipping_query_id=self.id,
            ok=ok,
            shipping_options=shipping_options,
            error_message=error_message,
        )
