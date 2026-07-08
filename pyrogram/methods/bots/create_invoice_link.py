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
from typing import List, Optional, Union

import pyrogram
from pyrogram import types


class CreateInvoiceLink:
    async def create_invoice_link(
        self: "pyrogram.Client",
        title: str,
        description: str,
        payload: Union[str, bytes],
        currency: str,
        prices: List["types.LabeledPrice"],
        provider_token: Optional[str] = None,
        subscription_period: Optional[Union[int, timedelta]] = None,
        max_tip_amount: Optional[int] = None,
        suggested_tip_amounts: Optional[List[int]] = None,
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
        """Create an invoice link.

        This is a parity convenience wrapper that delegates to
        :meth:`~pyrogram.Client.create_invoice_link` from the payments surface.

        .. include:: /_includes/usable-by/bots.rst

        Returns:
            ``str``: On success, the invoice URL is returned.
        """
        return await pyrogram.methods.payments.create_invoice_link.CreateInvoiceLink.create_invoice_link(
            self,
            title=title,
            description=description,
            payload=payload,
            currency=currency,
            prices=prices,
            provider_token=provider_token,
            subscription_period=subscription_period,
            max_tip_amount=max_tip_amount,
            suggested_tip_amounts=suggested_tip_amounts,
            start_parameter=start_parameter,
            provider_data=provider_data,
            photo_url=photo_url,
            photo_size=photo_size,
            photo_width=photo_width,
            photo_height=photo_height,
            need_name=need_name,
            need_phone_number=need_phone_number,
            need_email=need_email,
            need_shipping_address=need_shipping_address,
            send_phone_number_to_provider=send_phone_number_to_provider,
            send_email_to_provider=send_email_to_provider,
            is_flexible=is_flexible,
        )
