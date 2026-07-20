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


from typing import TYPE_CHECKING

import pyrogram
from pyrogram import raw, utils
from pyrogram.types.object import Object

if TYPE_CHECKING:
    from datetime import datetime


class ReadParticipant(Object):
    """Contains information about a read participant.

    Parameters
    ----------
        user (:obj:`~pyrogram.types.User`):
            User who read the message.

        date (:py:obj:`~datetime.datetime`):
            Date the message was read.

    """

    def __init__(
        self,
        *,
        client: "pyrogram.Client" = None,
        user_id: "pyrogram.types.User",
        date: "datetime",
    ) -> None:
        super().__init__(client)

        self.user = user_id
        self.date = date

    @staticmethod
    async def _parse(
        client,
        read_participant: "raw.base.ReadParticipantDate",
    ) -> "ReadParticipant":
        return ReadParticipant(
            client=client,
            user_id=await client.get_users(read_participant.user_id),
            date=utils.timestamp_to_datetime(read_participant.date),
        )
