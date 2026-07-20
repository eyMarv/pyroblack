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


class RefundStarPayment:
    async def refund_star_payment(
        self: pyrogram.Client,
        user_id: int | str,
        telegram_payment_charge_id: str,
    ) -> bool:
        """Refunds a successful payment in `Telegram Stars <https://t.me/BotNews/90>`_.

        .. include:: /_includes/usable-by/bots.rst

        Parameters
        ----------
            user_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target user, whose payment will be refunded.

            telegram_payment_charge_id (``str``):
                Telegram payment identifier.

        Returns
        -------
            ``bool``: True on success

        """
        r = await self.invoke(
            raw.functions.payments.RefundStarsCharge(
                user_id=await self.resolve_peer(user_id),
                charge_id=telegram_payment_charge_id,
            ),
        )
        return bool(r)
