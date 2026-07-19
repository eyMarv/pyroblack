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


class GetStarsBalance:
    async def get_stars_balance(
        self: pyrogram.Client,
        chat_id: int | str | None = None,
    ) -> float:
        """Get the current Telegram Stars balance of the current account.

        .. include:: /_includes/usable-by/users-bots.rst

        Parameters
        ----------
            chat_id (``int`` | ``str``, *optional*):
                Unique identifier (int) or username (str) of the target chat.
                For your personal cloud (Saved Messages) you can simply use "me" or "self".

        Returns
        -------
            ``float``: On success, the current stars balance is returned.

        Example:
            .. code-block:: python

                # Get stars balance of current account
                await app.get_stars_balance()

                # Get stars balance of a bot
                await app.get_stars_balance(chat_id="pyrogrambot")

        """
        if chat_id is None:
            peer = raw.types.InputPeerSelf()
        else:
            peer = await self.resolve_peer(chat_id)

        r = await self.invoke(
            raw.functions.payments.GetStarsTransactions(
                peer=peer,
                offset="",
                limit=0,
            ),
        )

        return r.balance.amount + r.balance.nanos / 1e9
