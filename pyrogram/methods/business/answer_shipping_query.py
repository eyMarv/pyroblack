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

from __future__ import annotations

import pyrogram
from pyrogram import raw, types


class AnswerShippingQuery:
    async def answer_shipping_query(
        self: pyrogram.Client,
        shipping_query_id: str,
        ok: bool,
        shipping_options: list[types.ShippingOptions] | None = None,
        error_message: str | None = None,
    ):
        """If you sent an invoice requesting a shipping address and the parameter ``is_flexible`` was specified, the API sends the confirmation in the form of an :obj:`~pyrogram.handlers.ShippingQueryHandler`.

        Use this method to reply to shipping queries.

        .. include:: /_includes/usable-by/bots.rst

        Parameters
        ----------
            shipping_query_id (``str``):
                Unique identifier for the query to be answered.

            ok (``bool``):
                Specify True if everything is alright (goods are available, etc.) and the bot is ready to proceed with the order. Use False if there are any problems.

            shipping_options (List of :obj:`~pyrogram.types.ShippingOptions`, *optional*):
                Required if ok is True. A array of available shipping options.

            error_message (``str``, *optional*):
                Required if ok is False. Error message in human readable form that explains the reason for failure to proceed with the checkout (e.g. "Sorry, somebody just bought the last of our amazing black T-shirts while you were busy filling out your payment details. Please choose a different color or garment!"). Telegram will display this message to the user.

        Returns
        -------
            ``bool``: True, on success.

        Example:
            .. code-block:: python

                # Proceed with the order
                await app.answer_shipping_query(query_id, ok=True, shipping_options=shipping_options)

                # Answer with error message
                await app.answer_shipping_query(query_id, ok=False, error_message="Error Message displayed to the user")

        """
        r = None
        if ok:
            r = await self.invoke(
                raw.functions.messages.SetBotShippingResults(
                    query_id=int(shipping_query_id),
                    shipping_options=[so.write() for so in shipping_options],
                ),
            )
        else:
            r = await self.invoke(
                raw.functions.messages.SetBotShippingResults(
                    query_id=int(shipping_query_id),
                    error=error_message or None,
                ),
            )
        return r
