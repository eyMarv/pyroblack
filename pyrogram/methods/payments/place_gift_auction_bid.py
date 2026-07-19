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


class PlaceGiftAuctionBid:
    async def place_gift_auction_bid(
        self: pyrogram.Client,
        gift_id: int,
        star_count: int,
        user_id: int | str | None = None,
        text: str | types.FormattedText | None = None,
        is_private: bool | None = False,
    ) -> bool:
        """Places a bid on an auction gift.

        .. include:: /_includes/usable-by/users.rst

        Parameters
        ----------
            gift_id (``int``):
                Identifier of the gift to place the bid on.

            star_count (``int``):
                The number of Telegram Stars to place in the bid.

            user_id (``int`` | ``str``, *optional*):
                Unique identifier (int) or username (str) of the target chat you want to transfer the star gift to.
                For your personal cloud (Saved Messages) you can simply use "me" or "self".
                For a contact that exists in your Telegram address book you can use his phone number (str).

            text (``str`` | :obj:`~pyrogram.types.FormattedText`, *optional*):
                Text to show along with the gift.
                Must be empty if the receiver enabled paid messages.

            is_private (``bool``, *optional*):
                Pass True to show gift text and sender only to the gift receiver, otherwise, everyone will be able to see them.

        Returns
        -------
            ``bool``: On success, True is returned.

        Example:
            .. code-block:: python

                # Place a bid of 100 stars on a gift auction for yourself
                await app.place_gift_auction_bid(
                    gift_id=12345,
                    star_count=100
                )

                # Place a bid of 250 stars on a gift auction for another user with a message
                await app.place_gift_auction_bid(
                    gift_id=12345,
                    star_count=250,
                    user_id="@KurimuzonAkuma",
                    text=types.FormattedText(
                        text="Here's a gift for you!"
                    )
                )

        """
        if isinstance(text, str):
            text = types.FormattedText(text=text)

        invoice = raw.types.InputInvoiceStarGiftAuctionBid(
            gift_id=gift_id,
            bid_amount=star_count,
            hide_name=is_private,
            update_bid=False,
            peer=await self.resolve_peer(user_id or "me"),
            message=await text.write() if text else None,
        )

        form = await self.invoke(
            raw.functions.payments.GetPaymentForm(
                invoice=invoice,
            ),
        )

        if star_count < 0:
            msg = "Invalid amount of Telegram Stars specified."
            raise ValueError(msg)

        if form.invoice.prices[0].amount > star_count:
            msg = "Have not enough Telegram Stars."
            raise ValueError(msg)

        r = await self.invoke(
            raw.functions.payments.SendStarsForm(
                form_id=form.form_id,
                invoice=invoice,
            ),
        )

        return isinstance(r, raw.types.payments.PaymentResult)
