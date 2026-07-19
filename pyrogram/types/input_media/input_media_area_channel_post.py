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

from .input_media_area import InputMediaArea


class InputMediaAreaChannelPost(InputMediaArea):
    """A channel post media area.

    Parameters
    ----------
        coordinates (:obj:`~pyrogram.types.MediaAreaCoordinates`):
            Media area coordinates.

        chat_id (``int`` | ``str``):
            Unique identifier (int) or username (str) of the target channel.

        message_id (``int``):
            A single message id.

    """

    def __init__(
        self,
        coordinates: types.MediaAreaCoordinates,
        chat_id: int | str,
        message_id: int,
    ) -> None:
        super().__init__(coordinates=coordinates)

        self.coordinates = coordinates
        self.chat_id = chat_id
        self.message_id = message_id

    async def write(self, client: pyrogram.Client):
        return raw.types.InputMediaAreaChannelPost(
            coordinates=self.coordinates,
            channel=await client.resolve_peer(self.chat_id),
            msg_id=self.message_id,
        )
