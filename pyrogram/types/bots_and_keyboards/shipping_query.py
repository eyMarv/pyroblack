#  Pyrogram - Telegram MTProto API Client Library for Python
#  Copyright (C) 2017-present Dan <https://github.com/delivrance>
#
#  This file is part of Pyrogram.
#
#  Pyrogram is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Lesser General Public License as published
#  by the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  Pyrogram is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public License
#  along with Pyrogram.  If not, see <http://www.gnu.org/licenses/>.

import pyrogram
from pyrogram import types

from ..object import Object
from ..update import Update


class ShippingQuery(Object, Update):
    def __init__(
        self,
        *,
        client: "pyrogram.Client" = None,
        id: str,
        from_user: "types.User",
        invoice_payload=None,
        shipping_address: "types.ShippingAddress" = None,
    ):
        super().__init__(client)
        self.id = id
        self.from_user = from_user
        self.invoice_payload = invoice_payload
        self.shipping_address = shipping_address

    @staticmethod
    async def _parse(client: "pyrogram.Client", shipping_query, users) -> "ShippingQuery":
        try:
            payload = shipping_query.payload.decode()
        except (UnicodeDecodeError, AttributeError):
            payload = shipping_query.payload

        address = shipping_query.shipping_address

        return ShippingQuery(
            id=str(shipping_query.query_id),
            from_user=types.User._parse(client, users[shipping_query.user_id]),
            invoice_payload=payload,
            shipping_address=types.ShippingAddress(
                country_code=address.country_iso2,
                state=address.state,
                city=address.city,
                street_line1=address.street_line1,
                street_line2=address.street_line2,
                post_code=address.post_code,
            ),
            client=client,
        )

    async def answer(self, ok: bool, shipping_options=None, error_message: str = None):
        return await self._client.answer_shipping_query(
            shipping_query_id=self.id,
            ok=ok,
            shipping_options=shipping_options,
            error_message=error_message,
        )
