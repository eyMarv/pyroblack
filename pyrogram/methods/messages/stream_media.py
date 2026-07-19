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

import math
from asyncio import sleep
from typing import TYPE_CHECKING

import pyrogram
from pyrogram import types
from pyrogram.file_id import FileId

if TYPE_CHECKING:
    import io


class StreamMedia:
    async def stream_media(
        self: pyrogram.Client,
        message: types.Message | str,
        limit: int = 0,
        offset: int = 0,
    ) -> str | io.BytesIO | None:
        """Stream the media from a message chunk by chunk.

        You can use this method to partially download a file into memory or to selectively download chunks of file.
        The chunk maximum size is 1 MiB (1024 * 1024 bytes).

        .. include:: /_includes/usable-by/users-bots.rst

        Parameters
        ----------
            message (:obj:`~pyrogram.types.Message` | ``str``):
                Pass a Message containing the media, the media itself (message.audio, message.video, ...) or a file id
                as string.

            limit (``int``, *optional*):
                Limit the amount of chunks to stream.
                Defaults to 0 (stream the whole media).

            offset (``int``, *optional*):
                How many chunks to skip before starting to stream.
                Defaults to 0 (start from the beginning).

        Returns
        -------
            ``Generator``: A generator yielding bytes chunk by chunk

        Example:
            .. code-block:: python

                # Stream the whole media
                async for chunk in app.stream_media(message):
                    print(len(chunk))

                # Stream the first 3 chunks only
                async for chunk in app.stream_media(message, limit=3):
                    print(len(chunk))

                # Stream the rest of the media by skipping the first 3 chunks
                async for chunk in app.stream_media(message, offset=3):
                    print(len(chunk))

                # Stream the last 3 chunks only (negative offset)
                async for chunk in app.stream_media(message, offset=-3):
                    print(len(chunk))

        """
        available_media = (
            "audio",
            "document",
            "photo",
            "sticker",
            "animation",
            "video",
            "voice",
            "video_note",
            "new_chat_photo",
        )

        if isinstance(message, types.Message):
            for kind in available_media:
                media = getattr(message, kind, None)

                if media is not None:
                    break
            else:
                msg = "This message doesn't contain any downloadable media"
                raise ValueError(msg)
        else:
            media = message
        # TODO
        file_id_str = media if isinstance(media, str) else media.file_id

        file_id_obj = FileId.decode(file_id_str)
        file_size = getattr(media, "file_size", 0)

        if offset < 0:
            if file_size == 0:
                msg = "Negative offsets are not supported for file ids, pass a Message object instead"
                raise ValueError(msg)

            chunks = math.ceil(file_size / 1024 / 1024)
            offset += chunks

        async for chunk in self.get_file(file_id_obj, file_size, limit, offset):
            await sleep(0)
            yield chunk
