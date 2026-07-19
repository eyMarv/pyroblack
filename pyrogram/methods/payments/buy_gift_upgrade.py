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


class BuyGiftUpgrade:
    async def buy_gift_upgrade(
        self: pyrogram.Client,
        owner_id: int | str,
        prepaid_upgrade_hash: str,
        star_count: int,
    ) -> types.Message | None:
        """Pays for upgrade of a regular gift that is owned by another user or channel chat.

        .. include:: /_includes/usable-by/users.rst

        Parameters
        ----------
            owner_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target chat.
                For a contact that exists in your Telegram address book you can use his phone number (str).

            prepaid_upgrade_hash (``str``):
                Prepaid upgrade hash as received along with the gift.

            star_count (``int``, *optional*):
                The amount of Telegram Stars the user agreed to pay for the upgrade.
                Must be equal to gift.upgrade_price.

        Returns
        -------
            ``bool``: On success, True is returned.

        """
        invoice = raw.types.InputInvoiceStarGiftPrepaidUpgrade(
            peer=await self.resolve_peer(owner_id),
            hash=prepaid_upgrade_hash,
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

        await self.invoke(
            raw.functions.payments.SendStarsForm(
                form_id=form.form_id,
                invoice=invoice,
            ),
        )

        return True
