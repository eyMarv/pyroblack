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

from typing import Union

import pyrogram
from pyrogram import raw


class EditUserStarSubscription:
    async def edit_user_star_subscription(
        self: "pyrogram.Client",
        user_id: Union[int, str],
        telegram_payment_charge_id: str,
        is_canceled: bool,
    ) -> bool:
        """Cancels or re-enables Telegram Star subscription for a user.

        .. include:: /_includes/usable-by/bots.rst

        Parameters:
            user_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target user.

            telegram_payment_charge_id (``str``):
                Telegram payment identifier of the subscription.

            is_canceled (``bool``):
                Pass True to cancel the subscription.
                Pass False to allow the user to enable it.

        Returns:
            ``bool``: On success, True is returned.
        """
        return await self.invoke(
            raw.functions.payments.BotCancelStarsSubscription(
                user_id=await self.resolve_peer(user_id),
                charge_id=telegram_payment_charge_id,
                restore=is_canceled,
            )
        )
