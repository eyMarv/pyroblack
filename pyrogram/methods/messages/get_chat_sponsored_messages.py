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


class GetChatSponsoredMessages:
    async def get_chat_sponsored_messages(
        self: pyrogram.Client,
        chat_id: int | str,
    ) -> list[types.SponsoredMessage] | None:
        """Returns sponsored messages to be shown in a chat; for channel chats only.

        .. include:: /_includes/usable-by/users.rst

        Parameters
        ----------
            chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target chat.

        Returns
        -------
            List of :obj:`~pyrogram.types.SponsoredMessage`: a list of sponsored messages is returned.

        Example:
            .. code-block:: python

                # Get a sponsored messages
                sm = await app.get_chat_sponsored_messages(chat_id)
                print(sm)

        """
        r = await self.invoke(
            raw.functions.messages.GetSponsoredMessages(
                peer=await self.resolve_peer(chat_id),
            ),
        )

        if isinstance(r, raw.types.messages.SponsoredMessagesEmpty):
            return None

        users = {i.id: i for i in r.users}

        return types.List(
            [types.SponsoredMessage._parse(self, sm, users) for sm in r.messages]
        )
