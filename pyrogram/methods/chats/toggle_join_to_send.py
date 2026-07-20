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
from pyrogram import errors, raw


class ToggleJoinToSend:
    async def toggle_join_to_send(
        self: pyrogram.Client,
        chat_id: int | str,
        enabled: bool = False,
    ) -> bool:
        """Enable or disable guest users' ability to send messages in a supergroup.

        .. include:: /_includes/usable-by/users.rst

        Parameters
        ----------
            chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target chat.

            enabled (``bool``):
                The new status. Pass True to enable guest users to send message.

        Returns
        -------
            ``bool``: True on success. False otherwise.

        Example:
            .. code-block:: python

                # Change status of guests sending messages to disabled
                await app.toggle_join_to_send()

                # Change status of guests sending messages to enabled
                await app.toggle_join_to_send(enabled=True)

        """
        try:
            r = await self.invoke(
                raw.functions.channels.ToggleJoinToSend(
                    channel=await self.resolve_peer(chat_id),
                    enabled=enabled,
                ),
            )

            return bool(r)
        except errors.RPCError:
            return False
