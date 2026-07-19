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
from pyrogram import types


class GetMessageReadParticipants:
    async def get_message_read_participants(
        self: pyrogram.Client,
        chat_id: int | str,
        message_id: int,
    ):
        """Get the list of users who have read a message.

        .. include:: /_includes/usable-by/users.rst

        Parameters
        ----------
            chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target chat.
                You can also use chat public link in form of *t.me/<username>* (str).

            message_id (``int``):
                Unique identifier of the target message.

        Returns
        -------
            ``AsyncGenerator``: On success, an async generator yielding :obj:`~pyrogram.types.ReadParticipant` objects is returned.

        """
        peer = await self.resolve_peer(chat_id)
        r = await self.invoke(
            pyrogram.raw.functions.messages.GetMessageReadParticipants(
                peer=peer,
                msg_id=message_id,
            ),
        )
        for read_participant in r:
            yield await types.ReadParticipant._parse(
                client=self,
                read_participant=read_participant,
            )
