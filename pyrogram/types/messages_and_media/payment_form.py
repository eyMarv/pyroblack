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

from typing import Optional

import pyrogram
from pyrogram import enums, raw, types
from ..object import Object


class PaymentForm(Object):
    """This object contains information about a payment form.

    Parameters:
        id (``int``):
            Form id.

        type (:obj:`~pyrogram.enums.PaymentFormType`):
            Type of the payment form.

        bot (``str``, *optional*):
            Seller bot.

        title (``str``):
            Form title.

        description (``str``):
            Form description.

        invoice (``str``):
            Invoice.

        provider (``str``, *optional*):
            Payment provider.

        url (``str``, *optional*):
            Payment form URL.

        can_save_credentials (``str``, *optional*):
            Whether the user can choose to save credentials.

        is_password_missing (``str``, *optional*):
            Indicates that the user can save payment credentials,
            but only after setting up a 2FA password
            (currently the account doesn't have a 2FA password).

        native_provider (``str``, *optional*):
            Payment provider name.

        additional_payment_options (List of :obj:`~pyrogram.types.PaymentOption`, *optional*):
            Additional payment options.

        saved_credentials (List of :obj:`~pyrogram.types.SavedCredentials`, *optional*):
            Saved payment credentials.
    """

    def __init__(
        self,
        *,
        client: "pyrogram.Client" = None,
        id: int,
        type: "enums.PaymentFormType",
        bot: "types.User" = None,
        title: str = None,
        description: str = None,
        invoice: "types.Invoice" = None,
        provider: Optional["types.User"] = None,
        url: Optional[str] = None,
        can_save_credentials: Optional[bool] = None,
        is_password_missing: Optional[bool] = None,
        native_provider: Optional[str] = None,
        additional_payment_options=None,
        saved_credentials=None,
        raw: "raw.base.payments.PaymentForm" = None,
    ):
        super().__init__(client)

        self.id = id
        self.type = type
        self.bot = bot
        self.title = title
        self.description = description
        self.invoice = invoice
        self.provider = provider
        self.url = url
        self.can_save_credentials = can_save_credentials
        self.is_password_missing = is_password_missing
        self.native_provider = native_provider
        self.additional_payment_options = additional_payment_options
        self.saved_credentials = saved_credentials
        self.raw = raw

    @staticmethod
    def _parse(client, payment_form: "raw.base.payments.PaymentForm") -> "PaymentForm":
        users = {i.id: i for i in getattr(payment_form, "users", [])}

        if isinstance(payment_form, raw.types.payments.PaymentForm):
            return PaymentForm(
                id=payment_form.form_id,
                type=enums.PaymentFormType.REGULAR,
                bot=types.User._parse(client, users.get(payment_form.bot_id)),
                title=payment_form.title,
                description=payment_form.description,
                invoice=types.Invoice._parse(client, payment_form.invoice),
                provider=types.User._parse(client, users.get(getattr(payment_form, "provider_id", None))),
                url=getattr(payment_form, "url", None),
                can_save_credentials=getattr(payment_form, "can_save_credentials", None),
                is_password_missing=getattr(payment_form, "password_missing", None),
                native_provider=getattr(payment_form, "native_provider", None),
                additional_payment_options=types.List([
                    types.PaymentOption._parse(option)
                    for option in getattr(payment_form, "additional_methods", [])
                ]) or None,
                saved_credentials=types.List([
                    types.SavedCredentials._parse(credential)
                    for credential in getattr(payment_form, "saved_credentials", [])
                ]) or None,
                raw=payment_form,
            )

        if isinstance(payment_form, raw.types.payments.PaymentFormStarGift):
            return PaymentForm(
                id=payment_form.form_id,
                type=enums.PaymentFormType.STAR_SUBSCRIPTION,
                invoice=types.Invoice._parse(client, payment_form.invoice),
                raw=payment_form,
            )

        if isinstance(payment_form, raw.types.payments.PaymentFormStars):
            return PaymentForm(
                id=payment_form.form_id,
                type=enums.PaymentFormType.STARS,
                bot=types.User._parse(client, users.get(payment_form.bot_id)),
                title=payment_form.title,
                description=payment_form.description,
                invoice=types.Invoice._parse(client, payment_form.invoice),
                raw=payment_form,
            )

        return None
