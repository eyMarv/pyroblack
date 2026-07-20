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
from pyrogram import raw


class AnswerPreCheckoutQuery:
    async def answer_pre_checkout_query(
        self: pyrogram.Client,
        pre_checkout_query_id: str,
        success: bool | None = None,
        error: str | None = None,
    ):
        """Send answers to pre-checkout queries.

        .. include:: /_includes/usable-by/bots.rst

        Parameters
        ----------
            pre_checkout_query_id (``str``):
                Unique identifier for the query to be answered.

            success (``bool``, *optional*):
                Set this flag if everything is alright (goods are available, etc.) and the bot is ready to proceed with the order.
                Otherwise do not set it, and set the error field, instead.

            error (``str``, *optional*):
                Error message in human readable form that explains the reason for failure to proceed with the checkout.
                Required if ``success`` isn't set.

        Returns
        -------
            ``bool``: True, on success.

        Example:
            .. code-block:: python

                # Proceed with the order
                await app.answer_pre_checkout_query(query_id, success=True)

                # Answer with error message
                await app.answer_pre_checkout_query(query_id, error=error)

        """
        return await self.invoke(
            raw.functions.messages.SetBotPrecheckoutResults(
                query_id=int(pre_checkout_query_id),
                success=success or None,
                error=error or None,
            ),
        )
