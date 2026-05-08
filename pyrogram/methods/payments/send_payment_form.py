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

import re
from typing import Union

import pyrogram
from pyrogram import raw


class SendPaymentForm:
    async def send_payment_form(
        self: "pyrogram.Client",
        chat_id: Union[int, str],
        message_id: Union[int, str],
    ) -> bool:
        """Pay an invoice.

        .. note::

            For now only stars invoices are supported.

        .. include:: /_includes/usable-by/users.rst

        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target chat.
                Unique identifier for the target chat in form of a *t.me/joinchat/* link, identifier (int) or username
                of the target channel/supergroup (in the format @username).

            message_id (``int`` | ``str``):
                Pass a message identifier or to get the invoice from message.
                Pass a invoice link in form of a *t.me/$...* link or slug itself to get the payment form from link.

        Returns:
            ``bool``: On success, True is returned.

        Example:
            .. code-block:: python

                # Pay invoice from message
                app.send_payment_form(chat_id, 123)

                # Pay invoice form from link
                # Chat id can be None
                app.send_payment_form(chat_id, "https://t.me/$xvbzUtt5sUlJCAAATqZrWRy9Yzk")
        """
        invoice = None

        if isinstance(message_id, int):
            invoice = raw.functions.InputInvoiceMessage(
                peer=await self.resolve_peer(chat_id), msg_id=message_id
            )
        elif isinstance(message_id, str):
            match = re.match(
                r"^(?:https?://)?(?:www\.)?(?:t(?:elegram)?\.(?:org|me|dog)/\$)([\w-]+)$",
                message_id,
            )

            if match:
                slug = match.group(1)
            else:
                slug = message_id

            invoice = raw.functions.InputInvoiceSlug(slug=slug)

        form = await self.get_payment_form(chat_id=chat_id, message_id=message_id)

        # if form.invoice.currency == "XTR":
        await self.invoke(
            raw.functions.payments.SendStarsForm(form_id=form.id, invoice=invoice)
        )
        # TODO: Add support for regular invoices (credentials)
        # else:
        #     r = await self.invoke(
        #         raw.functions.payments.SendPaymentForm(
        #             form_id=form.id,
        #             invoice=invoice,
        #             credentials=raw.functions.InputPaymentCredentials(data=raw.functions.DataJSON(data={}))
        #         )
        #     )

        return True
