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

import pyrogram
from pyrogram import raw, utils
from pyrogram.file_id import FileType


class SaveGif:
    async def save_gif(
        self: "pyrogram.Client",
        file_id: str,
        unsave: bool = False,
    ) -> bool:
        """Add or remove a gif from the saved gifs list.

        .. include:: /_includes/usable-by/users.rst

        Parameters:
            file_id (``str``):
                A file_id from a gif message.

            unsave (``bool``, *optional*):
                Pass True to remove the gif from saved gifs.

        Returns:
            ``bool``: True on success.
        """
        input_doc = utils.get_input_media_from_file_id(file_id, FileType.ANIMATION)

        return bool(
            await self.invoke(
                raw.functions.messages.SaveGif(
                    id=input_doc.id,
                    unsave=unsave,
                )
            )
        )
