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
from pyrogram import raw, utils
from pyrogram.file_id import FileType


class RemoveProfileAudio:
    async def remove_profile_audio(
        self: "pyrogram.Client",
        audio: str,
    ):
        """Removes an audio file from the profile audio files of the current user.

        .. include:: /_includes/usable-by/users.rst

        Parameters
        ----------
            audio (``str``):
                Identifier of the audio file to be removed.
                Use :meth:`~pyrogram.Client.get_chat_audios` to get the Audio identifier.

        Returns
        -------
            ``bool``: On success, True is returned.

        Example:
            .. code-block:: python

                # Remove audio file from profile
                await app.remove_profile_audio(file_id)

        """
        return await self.invoke(
            raw.functions.account.SaveMusic(
                id=(utils.get_input_media_from_file_id(audio, FileType.AUDIO)).id,
                unsave=True,
            ),
        )
