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

from datetime import timedelta
from typing import Optional, Union

import pyrogram
from pyrogram import raw, types


class CreateInvoiceLink:
    async def create_invoice_link(
        self: "pyrogram.Client",
        title: str,
        description: str,
        payload: Union[str, bytes],
        currency: str,
        prices: list["types.LabeledPrice"],
        provider_token: Optional[str] = None,
        subscription_period: Optional[Union[int, timedelta]] = None,
        max_tip_amount: Optional[int] = None,
        suggested_tip_amounts: Optional[list[int]] = None,
        start_parameter: Optional[str] = None,
        provider_data: Optional[str] = None,
        photo_url: Optional[str] = None,
        photo_size: Optional[int] = None,
        photo_width: Optional[int] = None,
        photo_height: Optional[int] = None,
        need_name: Optional[bool] = None,
        need_phone_number: Optional[bool] = None,
        need_email: Optional[bool] = None,
        need_shipping_address: Optional[bool] = None,
        send_phone_number_to_provider: Optional[bool] = None,
        send_email_to_provider: Optional[bool] = None,
        is_flexible: Optional[bool] = None,
    ) -> str:
        rpc = raw.functions.payments.ExportInvoice(
            invoice_media=raw.types.InputMediaInvoice(
                title=title,
                description=description,
                photo=(
                    raw.types.InputWebDocument(
                        url=photo_url,
                        mime_type="image/jpg",
                        size=photo_size,
                        attributes=[
                            raw.types.DocumentAttributeImageSize(
                                w=photo_width,
                                h=photo_height,
                            )
                        ],
                    )
                    if photo_url
                    else None
                ),
                invoice=raw.types.Invoice(
                    currency=currency,
                    prices=[i.write() for i in prices],
                    test=self.test_mode,
                    name_requested=need_name,
                    phone_requested=need_phone_number,
                    email_requested=need_email,
                    shipping_address_requested=need_shipping_address,
                    flexible=is_flexible,
                    phone_to_provider=send_phone_number_to_provider,
                    email_to_provider=send_email_to_provider,
                    max_tip_amount=max_tip_amount,
                    suggested_tip_amounts=suggested_tip_amounts,
                    subscription_period=(
                        int(subscription_period.total_seconds())
                        if isinstance(subscription_period, timedelta)
                        else subscription_period
                    ) if subscription_period else None,
                ),
                payload=payload.encode() if isinstance(payload, str) else payload,
                provider=provider_token,
                provider_data=raw.types.DataJSON(data=provider_data if provider_data else "{}"),
                start_param=start_parameter,
            )
        )
        r = await self.invoke(rpc)
        return r.url
