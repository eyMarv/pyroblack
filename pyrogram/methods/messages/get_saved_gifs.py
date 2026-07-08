#  Pyrogram - Telegram MTProto API Client Library for Python
#  Copyright (C) 2017-present Dan <https://github.com/delivrance>
#
#  This file is part of Pyrogram.
#
#  Pyrogram is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Lesser General Public License as published
#  by the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  Pyrogram is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public License
#  along with Pyrogram.  If not, see <http://www.gnu.org/licenses/>.

from typing import AsyncGenerator, Optional

import pyrogram
from pyrogram import raw, types


class GetSavedGifs:
    async def get_saved_gifs(
        self: "pyrogram.Client",
        hash: int = 0,
    ) -> Optional[AsyncGenerator["types.Animation", None]]:
        """Get saved gifs.

        .. include:: /_includes/usable-by/users.rst

        Parameters:
            hash (``int``, *optional*):
                The hash value of the saved gifs.

        Returns:
            ``Generator``: A generator yielding :obj:`~pyrogram.types.Animation` objects.
        """
        r = await self.invoke(
            raw.functions.messages.GetSavedGifs(hash=hash)
        )

        for gif in r.gifs:
            attributes = {type(i): i for i in gif.attributes}
            video_attributes = attributes.get(raw.types.DocumentAttributeVideo, None)
            yield types.Animation._parse(self, gif, video_attributes, gif.name)
