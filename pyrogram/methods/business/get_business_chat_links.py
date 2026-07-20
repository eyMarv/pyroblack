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

# ***************************
# GENERATED FILE - DO NOT EDIT
# Source: tl:account.getBusinessChatLinks
# ***************************


import pyrogram
from pyrogram import raw, types


class GetBusinessChatLinks:
    async def get_business_chat_links(
        self: "pyrogram.Client",
    ) -> "types.BusinessChatLinks":
        """Get all business chat links.

        .. include:: /_includes/usable-by/users.rst

        Returns:
            :obj:`~pyrogram.types.BusinessChatLinks`

        Example:
            .. code-block:: python

                await app.get_business_chat_links(...)

        """
        r = await self.invoke(
            raw.functions.account.getBusinessChatLinks(),
        )

        return types.BusinessChatLinks._parse(self, r)
