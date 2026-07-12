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
# Source: tl:account.createBusinessChatLink
# ***************************

from typing import Union, Optional

import pyrogram
from pyrogram import raw
from pyrogram import types


class CreateBusinessChatLink:
    async def create_business_chat_link(
        self: "pyrogram.Client",
        link: Optional[raw.types.InputBusinessChatLink] = None,
    ) -> "types.BusinessChatLink":
        """Create a business chat link with a predefined message.

        .. include:: /_includes/usable-by/users.rst

        Parameters:
            link (raw.types.InputBusinessChatLink): The chat link config (message, entities, title)

        Returns:
            :obj:`~pyrogram.types.BusinessChatLink`

        Example:
            .. code-block:: python

                await app.create_business_chat_link(...)
        """

        r = await self.invoke(
            raw.functions.account.createBusinessChatLink(
                link=link,
            )
        )
