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

from typing import TYPE_CHECKING

import pyrogram
from pyrogram import raw

if TYPE_CHECKING:
    import io


class SetProfilePhoto:
    # TODO: FIXME!
    async def set_profile_photo(
        self: pyrogram.Client,
        *,
        photo: str | io.BytesIO | None = None,
        video: str | io.BytesIO | None = None,
        public: bool = False,
        for_my_bot: int | str | None = None,
        photo_frame_start_timestamp: float | None = None,
        **kwargs,
    ) -> bool:
        """Set a new profile photo or video (H.264/MPEG-4 AVC video, max 5 seconds).

        The ``photo`` and ``video`` arguments are mutually exclusive.
        Pass either one as named argument (see examples below).

        .. include:: /_includes/usable-by/users-bots.rst

        Parameters
        ----------
            photo (``str`` | :obj:`io.BytesIO`, *optional*):
                Profile photo to set.
                Pass a file path as string to upload a new photo that exists on your local machine or
                pass a binary file-like object with its attribute ".name" set for in-memory uploads.

            video (``str`` | :obj:`io.BytesIO`, *optional*):
                Profile video to set.
                Pass a file path as string to upload a new video that exists on your local machine or
                pass a binary file-like object with its attribute ".name" set for in-memory uploads.

            public (``bool``, *optional*):
                Pass True to upload a public profile photo for users who are restricted from viewing your real profile photos due to your privacy settings.
                Defaults to False.

            for_my_bot (``int`` | ``str``, *optional*):
                Unique identifier (int) or username (str) of the bot for which profile photo has to be updated instead of the current user.
                The bot should have ``can_be_edited`` property set to True.

            photo_frame_start_timestamp (``float``, *optional*):
                Floating point UNIX timestamp in seconds, indicating the frame of the video/sticker that should be used as static preview; can only be used if ``video`` is set.

        Returns
        -------
            ``bool``: True on success.

        Example:
            .. code-block:: python

                # Set a new profile photo
                await app.set_profile_photo(photo="new_photo.jpg")

                # Set a new profile video
                await app.set_profile_photo(video="new_video.mp4")

        """
        return bool(
            await self.invoke(
                raw.functions.photos.UploadProfilePhoto(
                    fallback=public,
                    file=await self.save_file(photo),
                    video=await self.save_file(video),
                    bot=await self.resolve_peer(for_my_bot) if for_my_bot else None,
                    video_start_ts=photo_frame_start_timestamp,
                ),
            ),
        )
