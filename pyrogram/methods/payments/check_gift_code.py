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

import pyrogram
from pyrogram import types


class CheckGiftCodeAlias:
    async def check_gift_code(
        self: "pyrogram.Client",
        link: str,
    ) -> "types.CheckedGiftCode":
        """Get information about a gift code.

        Alias of :meth:`~pyrogram.Client.check_giftcode` provided for naming
        parity with upstream forks.

        .. include:: /_includes/usable-by/users.rst

        Parameters:
            link (``str``):
                The gift code link.

        Returns:
            :obj:`~pyrogram.types.CheckedGiftCode`: On success, a checked gift code is returned.
        """
        return await pyrogram.methods.payments.check_giftcode.CheckGiftCode.check_gift_code(
            self, link=link
        )
