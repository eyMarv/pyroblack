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


class SetChatTitle:
    async def set_chat_title(
        self: pyrogram.Client,
        chat_id: int | str,
        title: str,
    ) -> types.Message | bool:
        """Change the title of a chat.
        Titles can't be changed for private chats.
        You must be an administrator in the chat for this to work and must have the appropriate admin rights.

        Note:
            In regular groups (non-supergroups), this method will only work if the "All Members Are Admins"
            setting is off.

        .. include:: /_includes/usable-by/users-bots.rst

        Parameters
        ----------
            chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target chat.

            title (``str``):
                New chat title, 1-255 characters.

        Returns
        -------
            :obj:`~pyrogram.types.Message` | ``bool``: On success, a service message will be returned (when applicable),
            otherwise, in case a message object couldn't be returned, True is returned.

        Raises
        ------
            ValueError: In case a chat id belongs to user.

        Example:
            .. code-block:: python

                await app.set_chat_title(chat_id, "New Title")

        """
        peer = await self.resolve_peer(chat_id)

        if isinstance(peer, raw.types.InputPeerChat):
            r = await self.invoke(
                raw.functions.messages.EditChatTitle(
                    chat_id=peer.chat_id,
                    title=title,
                ),
            )
        elif isinstance(peer, raw.types.InputPeerChannel):
            r = await self.invoke(
                raw.functions.channels.EditTitle(
                    channel=peer,
                    title=title,
                ),
            )
        else:
            msg = f'The chat_id "{chat_id}" belongs to a user'
            raise ValueError(msg)

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
