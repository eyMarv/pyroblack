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


class SetChatMessageAutoDeleteTime:
    async def set_chat_message_auto_delete_time(
        self: pyrogram.Client,
        chat_id: int | str,
        message_auto_delete_time: int,
    ) -> types.Message | bool:
        """Changes the message auto-delete or self-destruct (for secret chats) time in a chat.

        Requires change_info administrator right in basic groups, supergroups and channels.

        .. include:: /_includes/usable-by/users.rst

        Parameters
        ----------
            chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target chat.

            message_auto_delete_time (``int``):
                New time value, in seconds; unless the chat is secret, it must be from 0 up to 365 * 86400 and be divisible by 86400. If 0, then messages aren't deleted automatically.

        Returns
        -------
            :obj:`~pyrogram.types.Message` | ``bool``: On success, a service message will be returned (when applicable),
            otherwise, in case a message object couldn't be returned, True is returned.

        Example:
            .. code-block:: python

                # Set message auto delete for a chat to 1 day
                app.set_chat_message_auto_delete_time(chat_id, 86400)

                # Set message auto delete for a chat to 1 week
                app.set_chat_message_auto_delete_time(chat_id, 604800)

                # Disable message auto delete for this chat
                app.set_chat_message_auto_delete_time(chat_id, 0)

        """
        r = await self.invoke(
            raw.functions.messages.SetHistoryTTL(
                peer=await self.resolve_peer(chat_id),
                period=message_auto_delete_time,
            ),
        )

        for i in r.updates:
            if isinstance(
                i, (raw.types.UpdateNewMessage, raw.types.UpdateNewChannelMessage)
            ):
                return await types.Message._parse(
                    self,
                    i.message,
                    {i.id: i for i in r.users},
                    {i.id: i for i in r.chats},
                    replies=self.fetch_replies,
                )
        return True
