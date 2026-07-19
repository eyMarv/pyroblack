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


class DeleteAllMessageReactions:
    async def delete_all_message_reactions(
        self: pyrogram.Client,
        chat_id: int | str,
        *,
        user_id: int | str | None = None,
        actor_chat_id: int | str | None = None,
    ) -> bool:
        """Use this method to remove up to 10000 recent reactions in a group or a supergroup chat added by a given user or chat.

        .. note::

            The bot must have the `can_delete_messages` administrator right in the chat.

        .. include:: /_includes/usable-by/users-bots.rst

        Parameters
        ----------
            chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target chat.

            user_id (``int`` | ``str``, *optional*):
                Unique identifier (int) or username (str) of the user whose reactions will be removed, if the reactions were added by a user.

            actor_chat_id (``int`` | ``str``, *optional*):
                Unique identifier (int) or username (str) of the chat whose reactions will be removed, if the reactions were added by a chat.

        Returns
        -------
            ``bool``: True on success, False otherwise.

        """
        peer = None

        if user_id is not None:
            peer = await self.resolve_peer(user_id)

            if not isinstance(peer, (raw.types.InputPeerUser, raw.types.InputPeerSelf)):
                return False
        elif actor_chat_id is not None:
            peer = await self.resolve_peer(actor_chat_id)

            if not isinstance(peer, raw.types.InputPeerChannel):
                return False
        else:
            msg = "Invalid user_id or actor_chat_id"
            raise ValueError(msg)

        return await self.invoke(
            raw.functions.messages.DeleteParticipantReactions(
                peer=await self.resolve_peer(chat_id),
                participant=peer,
            ),
        )
