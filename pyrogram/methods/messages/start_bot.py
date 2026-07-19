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


class StartBot:
    async def start_bot(
        self: pyrogram.Client,
        chat_id: int | str,
        param: str = "",
    ) -> types.Message:
        """Start bot.

        .. include:: /_includes/usable-by/users.rst

        Parameters
        ----------
            chat_id (``int`` | ``str``):
                Unique identifier of the bot you want to be started. You can specify
                a @username (str) or a bot ID (int).

            param (``str``):
                Text of the deep linking parameter (up to 64 characters).
                Defaults to "" (empty string).

        Returns
        -------
            :obj:`~pyrogram.types.Message`: On success, the sent message is returned.

        Example:
            .. code-block:: python

                # Start bot
                await app.start_bot("pyrogrambot")

                # Start bot with param
                await app.start_bot("pyrogrambot", "ref123456")

        """
        if not param:
            return await self.send_message(chat_id, "/start")

        peer = await self.resolve_peer(chat_id)

        r = await self.invoke(
            raw.functions.messages.StartBot(
                bot=peer,
                peer=peer,
                random_id=self.rnd_id(),
                start_param=param,
            ),
        )

        for i in r.updates:
            if isinstance(i, raw.types.UpdateNewMessage):
                return await types.Message._parse(
                    self,
                    i.message,
                    {i.id: i for i in r.users},
                    {i.id: i for i in r.chats},
                )
        return None
