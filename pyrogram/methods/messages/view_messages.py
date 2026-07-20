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


class ViewMessages:
    async def view_messages(
        self: pyrogram.Client,
        chat_id: int | str,
        message_ids: int | list[int] | None = None,
        message_id: int | list[int] | None = None,  # alias for <=2.7.2
        force_read: bool = True,
    ) -> bool:
        """Informs the server that messages are being viewed by the current user.

        .. include:: /_includes/usable-by/users.rst

        Parameters
        ----------
            chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target chat.

            message_ids (``int`` | List of ``int``):
                Identifier or list of message identifiers of the target message.

            force_read (``bool``, *optional*):
                Pass True to mark as read the specified messages and also increment the view counter.

        Returns
        -------
            ``bool``: On success, True is returned.

        Example:
            .. code-block:: python

                # Increment message views
                await app.view_messages(chat_id, 1)

        """
        if message_ids is None and message_id is not None:
            message_ids = message_id
        if message_ids is None:
            msg = "message_ids (or message_id) is required"
            raise ValueError(msg)
        ids = [message_ids] if not isinstance(message_ids, list) else message_ids

        r = await self.invoke(
            raw.functions.messages.GetMessagesViews(
                peer=await self.resolve_peer(chat_id),
                id=ids,
                increment=force_read,
            ),
        )

        return bool(r)
