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


class ApproveChatJoinRequest:
    async def approve_chat_join_request(
        self: pyrogram.Client,
        chat_id: int | str,
        user_id: int,
    ) -> bool:
        """Approve a chat join request.

        You must be an administrator in the chat for this to work and must have the *can_invite_users* administrator
        right.

        .. include:: /_includes/usable-by/users-bots.rst

        Parameters
        ----------
            chat_id (``int`` | ``str``):
                Unique identifier for the target chat or username of the target channel/supergroup
                (in the format @username).

            user_id (``int``):
                Unique identifier of the target user.

        Returns
        -------
            ``bool``: True on success.

        """
        await self.invoke(
            raw.functions.messages.HideChatJoinRequest(
                peer=await self.resolve_peer(chat_id),
                user_id=await self.resolve_peer(user_id),
                approved=True,
            ),
        )

        return True
