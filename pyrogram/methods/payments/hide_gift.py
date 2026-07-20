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

import pyrogram
from pyrogram import raw, utils


class HideGift:
    async def hide_gift(
        self: "pyrogram.Client",
        owned_gift_id: str,
    ) -> bool:
        """Hide gift on the current user's or the channel's profile page.

        .. note::

            Requires `can_post_messages` administrator right in the channel chat.

        .. include:: /_includes/usable-by/users.rst

        Parameters
        ----------
            owned_gift_id (``str``):
                Unique identifier of the target gift.
                For a user gift, you can use the message ID (str) of the gift message.
                For a channel gift, you can use the packed format `chatID_savedID` (str).
                For a upgraded gift, you can use the gift link.

        Returns
        -------
            ``bool``: On success, True is returned.

        Example:
            .. code-block:: python

                # Hide gift in user profile
                await app.hide_gift(owned_gift_id="123")

                # Hide gift in channel (owned_gift_id packed in format chatID_savedID)
                await app.hide_gift(owned_gift_id="123_456")

        """
        return await self.invoke(
            raw.functions.payments.SaveStarGift(
                stargift=await utils.get_input_stargift(self, owned_gift_id),
                unsave=True,
            ),
        )
