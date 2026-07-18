#  Pyroblack - Telegram MTProto API Client Library for Python
#  Copyright (C) 2017-2024 Dan <https://github.com/delivrance>
#  Copyright (C) 2024-present eyMarv <https://github.com/eyMarv>
#  Maintainer: irisXDR <https://github.com/irisXDR>
#
#  This file is part of Pyroblack.
#
#  Pyroblack is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Lesser General Public License as published
#  by the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  Pyroblack is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Lesser General Public License for more details.
#
#  Pyroblack is a continuation fork of Pyrogram <https://github.com/pyrogram/pyrogram>
#
#  You should have received a copy of the GNU Lesser General Public License
#  along with Pyroblack.  If not, see <http://www.gnu.org/licenses/>.

from typing import Optional, Union

import pyrogram
from pyrogram import raw, types


class GetPaymentForm:
    async def get_payment_form(
        self: "pyrogram.Client",
        input_invoice: "types.InputInvoice" = None,
        chat_id: Union[int, str] = None,
        message_id: Union[int, str] = None,
        invoice_link: str = None,
        **kwargs
    ) -> "types.PaymentForm":
        """Get an invoice payment form.

        Supports both modern ``input_invoice`` and pyroblack <= 2.7.2
        ``chat_id`` + ``message_id`` (or invoice link) call styles.

        .. include:: /_includes/usable-by/users.rst

        Parameters:
            input_invoice (:obj:`~pyrogram.types.InputInvoice`, *optional*):
                The invoice (modern API).

            chat_id (``int`` | ``str``, *optional*):
                Target chat (pyroblack <= 2.7.2 / positional style).

            message_id (``int`` | ``str``, *optional*):
                Message id with the invoice, or a ``t.me/$...`` link / slug
                (pyroblack <= 2.7.2 style).

            invoice_link (``str``, *optional*):
                Invoice link or slug.

        Returns:
            :obj:`~pyrogram.types.PaymentForm`: On success, a payment form is returned.
        """
        # Positional legacy: get_payment_form(chat_id, message_id)
        # First param may be chat_id (int/str) rather than InputInvoice.
        if input_invoice is not None and not hasattr(input_invoice, "write"):
            # get_payment_form(chat_id, message_id) binds as input_invoice=chat_id, chat_id=message_id
            if message_id is None and chat_id is not None:
                message_id = chat_id
                chat_id = input_invoice
            elif chat_id is None:
                chat_id = input_invoice
            input_invoice = None

        invoice = None

        if input_invoice is not None:
            invoice = await input_invoice.write(self)
        elif message_id is not None and isinstance(message_id, int) and chat_id is not None:
            invoice = raw.types.InputInvoiceMessage(
                peer=await self.resolve_peer(chat_id),
                msg_id=message_id
            )
        elif message_id is not None and isinstance(message_id, str):
            match = self.INVOICE_LINK_RE.match(message_id)
            slug = match.group(1) if match else message_id
            invoice = raw.types.InputInvoiceSlug(slug=slug)
        elif invoice_link is not None:
            match = self.INVOICE_LINK_RE.match(invoice_link)
            slug = match.group(1) if match else invoice_link
            invoice = raw.types.InputInvoiceSlug(slug=slug)
        else:
            raise ValueError(
                "Provide input_invoice, or chat_id+message_id, or invoice_link / message_id link."
            )

        r = await self.invoke(
            raw.functions.payments.GetPaymentForm(invoice=invoice)
        )

        return types.PaymentForm._parse(self, r)
