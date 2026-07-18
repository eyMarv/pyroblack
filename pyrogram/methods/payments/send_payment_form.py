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


class SendPaymentForm:
    async def send_payment_form(
        self: "pyrogram.Client",
        payment_form_id: int = None,
        input_invoice: "types.InputInvoice" = None,
        credentials: Optional["types.InputCredentials"] = None,
        chat_id: Union[int, str] = None,
        message_id: Union[int, str] = None,
        invoice_link: str = None,
        **kwargs
    ) -> Union[bool, "types.PaymentResult", list]:
        """Send a filled-out payment form / pay an invoice.

        Supports modern ``payment_form_id`` + ``input_invoice`` and pyroblack
        <= 2.7.2 ``chat_id`` + ``message_id`` (stars) call style.

        .. include:: /_includes/usable-by/users.rst

        Parameters:
            payment_form_id (``int``, *optional*):
                Payment form id from :meth:`~pyrogram.Client.get_payment_form`.

            input_invoice (:obj:`~pyrogram.types.InputInvoice`, *optional*):
                The invoice (modern API).

            credentials (:obj:`~pyrogram.types.InputCredentials`, *optional*):
                Payment credentials. None for Telegram Stars.

            chat_id (``int`` | ``str``, *optional*):
                Target chat (pyroblack <= 2.7.2).

            message_id (``int`` | ``str``, *optional*):
                Message id or invoice link/slug (pyroblack <= 2.7.2).

            invoice_link (``str``, *optional*):
                Invoice link or slug.

        Returns:
            ``bool`` | :obj:`~pyrogram.types.PaymentResult` | list: On success.
        """
        # Legacy positional: send_payment_form(chat_id, message_id)
        # Detect when first arg is chat id (not form id) — hard to distinguish ints.
        # Prefer keyword style from 2.7.2 bots; also accept chat_id=/message_id=.

        if (
            payment_form_id is not None
            and input_invoice is not None
            and hasattr(input_invoice, "write")
        ):
            if credentials is None:
                await self.invoke(
                    raw.functions.payments.SendStarsForm(
                        form_id=payment_form_id,
                        invoice=await input_invoice.write(self),
                    )
                )
            else:
                await self.invoke(
                    raw.functions.payments.SendPaymentForm(
                        form_id=payment_form_id,
                        invoice=await input_invoice.write(self),
                        credentials=await credentials.write(self)
                    )
                )
            return True

        # pyroblack <= 2.7.2: chat_id + message_id (or link)
        if not any((chat_id is not None and message_id is not None, invoice_link, message_id)):
            # maybe positional legacy: first param was chat_id stored in payment_form_id wrongly
            if payment_form_id is not None and input_invoice is not None and not hasattr(input_invoice, "write"):
                chat_id = payment_form_id
                message_id = input_invoice
                payment_form_id = None
                input_invoice = None

        invoice = None
        if message_id is not None and isinstance(message_id, int) and chat_id is not None:
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
                "Provide payment_form_id+input_invoice, or chat_id+message_id, or invoice_link."
            )

        form = await self.get_payment_form(
            chat_id=chat_id,
            message_id=message_id,
            invoice_link=invoice_link
        )

        await self.invoke(
            raw.functions.payments.SendStarsForm(
                form_id=form.id,
                invoice=invoice
            )
        )
        return True
