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

from typing import Union

import pyrogram


class RefundStarPaymentAlias:
    async def refund_star_payment(
        self: "pyrogram.Client",
        user_id: Union[int, str],
        telegram_payment_charge_id: str,
    ) -> bool:
        """Refund the star to the user.

        Alias of :meth:`~pyrogram.Client.refund_stars_payment` provided for
        naming parity with upstream forks.

        Parameters:
            user_id (``int`` | ``str``):
                The user id to refund the stars.

            telegram_payment_charge_id (``str``):
                The charge id to refund the stars.

        Returns:
            `bool`: On success, a True is returned.
        """
        return await pyrogram.methods.bots.refund_stars_payment.RefundStarPayment.refund_star_payment(
            self,
            user_id=user_id,
            telegram_payment_charge_id=telegram_payment_charge_id,
        )
