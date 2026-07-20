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
# Source: tl:account.resolveBusinessChatLink
# ***************************

from __future__ import annotations

import pyrogram
from pyrogram import raw, types


class ResolveBusinessChatLink:
    async def resolve_business_chat_link(
        self: pyrogram.Client,
        slug: str | None = None,
    ) -> types.Message:
        """Resolve a business chat link slug to its info.

        .. include:: /_includes/usable-by/users.rst

        Parameters
        ----------
            slug (str): Slug from the business chat link URL

        Returns
        -------
            :obj:`~pyrogram.types.Message`

        Example:
            .. code-block:: python

                await app.resolve_business_chat_link(...)

        """
        r = await self.invoke(
            raw.functions.account.resolveBusinessChatLink(
                slug=slug,
            ),
        )

        # API returns account.ResolvedBusinessChatLinks (peer + message text),
        # not a raw Message. Build a high-level Message-like reply content via Chat.
        from pyrogram import utils

        users = {i.id: i for i in r.users}
        chats = {i.id: i for i in r.chats}
        peer_id = utils.get_raw_peer_id(r.peer)
        if peer_id in users:
            chat = types.Chat._parse_user_chat(self, users[peer_id])
        else:
            chat = types.Chat._parse_chat(self, chats[peer_id])
        # Synthetic message so callers can still use .text / .chat
        return types.Message(
            id=0,
            chat=chat,
            text=r.message or None,
            client=self,
        )
