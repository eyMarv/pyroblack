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

import pyrogram
from pyrogram import raw, types
from pyrogram.types.object import Object


class MediaArea(Object):
    """Content of a media areas in story.

    It should be one of:

    - :obj:`~pyrogram.types.MediaAreaChannelPost`
    """

    def __init__(self, coordinates: "types.MediaAreaCoordinates") -> None:
        super().__init__()

        self.coordinates = coordinates

    @staticmethod
    async def _parse(
        client: "pyrogram.Client",
        media_area: "raw.base.MediaArea",
    ) -> "MediaArea":
        if isinstance(media_area, raw.types.MediaAreaChannelPost):
            try:
                return await types.MediaAreaChannelPost._parse(client, media_area)
            except Exception:
                return None
        return None
