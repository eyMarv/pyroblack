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
from pyrogram.utils import compute_password_check


class TransferChatOwnership:
    async def transfer_chat_ownership(
        self: pyrogram.Client,
        chat_id: int | str,
        user_id: int | str,
        password: str,
    ) -> bool:
        """Changes the owner of a chat.

        Requires owner privileges in the chat. Available only for supergroups and channel chats.

        .. include:: /_includes/usable-by/users.rst

        Parameters
        ----------
            chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target chat.

            user_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the new owner.
                The ownership can't be transferred to a bot or to a deleted user.

            password (``str``):
                The 2-step verification password of the current user.

        Returns
        -------
            ``bool``: True on success.

        Raises
        ------
            ValueError: In case of invalid parameters.
            :obj:`~pyrogram.errors.RPCError`: In case of a Telegram RPC error.

        Example:
            .. code-block:: python

                await app.transfer_chat_ownership(chat_id, user_id, "password")

        """
        peer_channel = await self.resolve_peer(chat_id)
        peer_user = await self.resolve_peer(user_id)

        if not isinstance(peer_channel, raw.types.InputPeerChannel):
            msg = "The chat_id must belong to a channel/supergroup."
            raise ValueError(msg)

        if not isinstance(peer_user, raw.types.InputPeerUser):
            msg = "The user_id must belong to a user."
            raise ValueError(msg)

        r = await self.invoke(
            raw.functions.channels.EditCreator(
                channel=peer_channel,
                user_id=peer_user,
                password=compute_password_check(
                    await self.invoke(raw.functions.account.GetPassword()),
                    password,
                ),
            ),
        )

        return bool(r)
