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

from typing import List, Optional

import pyrogram
from pyrogram import raw, types


class AnswerShippingQuery:
    async def answer_shipping_query(
        self: "pyrogram.Client",
        shipping_query_id: str,
        ok: bool,
        shipping_options: Optional[List["types.ShippingOption"]] = None,
        error_message: Optional[str] = None,
    ):
        if ok and not shipping_options:
            raise ValueError("Shipping options required.")

        return await self.invoke(
            raw.functions.messages.SetBotShippingResults(
                query_id=int(shipping_query_id),
                shipping_options=[so.write() for so in shipping_options] if shipping_options else None,
                error=error_message,
            )
        )
