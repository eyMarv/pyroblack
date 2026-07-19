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

from .input_story_content import InputStoryContent

if TYPE_CHECKING:
    import io


class InputStoryContentVideo(InputStoryContent):
    """Describes a video to post as a story.

    It is intended to be used with :obj:`~pyrogram.Client.send_story` or :obj:`~pyrogram.Client.post_story`.

    Parameters
    ----------
        video (``str`` | :obj:`io.BytesIO`):
            File to send.
            Pass a file_id as string to send a video that exists on the Telegram servers or
            pass a file path as string to upload a new video that exists on your local machine or
            pass a binary file-like object with its attribute “.name” set for in-memory uploads or
            pass an HTTP URL as a string for Telegram to get a video from the Internet.

        duration (``int``, *optional*):
            Precise duration of the video in seconds; 0-60.

        cover_frame_timestamp (``int``, *optional*):
            Timestamp in seconds of the frame that will be used as the static cover for the story. Defaults to 0.0.

        is_animation (``bool``, *optional*):
            Pass True if the video has no sound.

        width (``int``, *optional*):
            Video width.

        height (``int``, *optional*):
            Video height.

        thumbnail (``str`` | :obj:`io.BytesIO`):
            Thumbnail of the video sent.
            The thumbnail should be in JPEG format and less than 200 KB in size.
            A thumbnail's width and height should not exceed 320 pixels.
            Thumbnails can't be reused and can be only uploaded as a new file.

        supports_streaming (``bool``, *optional*):
            Pass True, if the uploaded video is suitable for streaming.

        file_name (``str``, *optional*):
            File name of the video sent.
            Defaults to file's path basename.

    """

    def __init__(
        self,
        video: str | io.BytesIO,
        duration: int = 0,
        cover_frame_timestamp: int = 0,
        is_animation: bool | None = None,
        width: int = 0,
        height: int = 0,
        thumbnail: str | io.BytesIO | None = None,
        supports_streaming: bool = True,
        file_name: str | None = None,
    ) -> None:
        super().__init__()

        self.video = video
        self.duration = duration
        self.cover_frame_timestamp = cover_frame_timestamp
        self.is_animation = is_animation
        self.width = width
        self.height = height
        self.thumbnail = thumbnail
        self.supports_streaming = supports_streaming
        self.file_name = file_name
