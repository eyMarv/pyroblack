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

import io
import os
import pathlib
import re
from typing import BinaryIO, Callable, List, Optional, Union

import pyrogram
from pyrogram import enums, raw, types
from pyrogram.file_id import FileId, FileType

from .input_media import InputMedia


class InputMediaLivePhoto(InputMedia):
    """Represents a live photo to be sent.

    Parameters:
        media (``str`` | ``BinaryIO``):
            Video of the live photo to send.
            Pass a file_id as string to send a video that exists on the Telegram servers or
            pass a file path as string to upload a new video that exists on your local machine or
            pass a binary file-like object with its attribute ".name" set for in-memory uploads or
            pass an HTTP URL as a string for Telegram to get a video from the Internet.

        photo (``str`` | ``BinaryIO``):
            The static photo to send.
            Pass a file_id as string to send a photo that exists on the Telegram servers or
            pass a file path as string to upload a new photo that exists on your local machine or
            pass a binary file-like object with its attribute ".name" set for in-memory uploads or
            pass an HTTP URL as a string for Telegram to get a photo from the Internet.

        caption (``str``, *optional*):
            Caption of the live photo to be sent, 0-1024 characters.
            If not specified, the original caption is kept. Pass "" (empty string) to remove the caption.

        parse_mode (:obj:`~pyrogram.enums.ParseMode`, *optional*):
            By default, texts are parsed using both Markdown and HTML styles.
            You can combine both syntaxes together.

        caption_entities (List of :obj:`~pyrogram.types.MessageEntity`):
            List of special entities that appear in the caption, which can be specified instead of *parse_mode*.

        show_caption_above_media (``bool``, *optional*):
            Pass True, if the caption must be shown above the message media.

        has_spoiler (``bool``, *optional*):
            Pass True if the photo needs to be covered with a spoiler animation.
    """

    def __init__(
        self,
        media: Union[str, BinaryIO],
        photo: Union[str, BinaryIO],
        thumb: Optional[str] = None,
        caption: str = "",
        parse_mode: Optional["enums.ParseMode"] = None,
        caption_entities: Optional[List["types.MessageEntity"]] = None,
        show_caption_above_media: Optional[bool] = None,
        has_spoiler: Optional[bool] = None,
    ):
        super().__init__(media, caption, parse_mode, caption_entities)

        self.photo = photo
        self.thumb = thumb
        self.show_caption_above_media = show_caption_above_media
        self.has_spoiler = has_spoiler

    async def write(
        self,
        client: "pyrogram.Client",
        chat_id: Optional[Union[int, str]] = None,
        business_connection_id: Optional[str] = None,
        progress: Optional[Callable] = None,
        progress_args: tuple = (),
        width: int = 0,
        height: int = 0,
    ):
        peer = await client.resolve_peer(chat_id or "me")

        is_bytes_io = isinstance(self.media, io.BytesIO) or isinstance(self.photo, io.BytesIO)
        is_uploaded_file = (
            is_bytes_io
            or (
                isinstance(self.media, (str, os.PathLike))
                and pathlib.Path(self.media).is_file()
            )
            or (
                isinstance(self.photo, (str, os.PathLike))
                and pathlib.Path(self.photo).is_file()
            )
        )

        if is_uploaded_file:
            uploaded_media = await client.invoke(
                raw.functions.messages.UploadMedia(
                    peer=peer,
                    media=raw.types.InputMediaUploadedDocument(
                        mime_type=client.guess_mime_type(self.media) or "video/mp4",
                        file=await client.save_file(
                            self.media, progress=progress, progress_args=progress_args
                        ),
                        spoiler=self.has_spoiler,
                        attributes=[
                            raw.types.DocumentAttributeVideo(
                                duration=0,
                                w=width,
                                h=height,
                            ),
                        ],
                    ),
                )
            )

            uploaded_photo = await client.invoke(
                raw.functions.messages.UploadMedia(
                    peer=peer,
                    media=raw.types.InputMediaUploadedPhoto(
                        file=await client.save_file(
                            self.photo, progress=progress, progress_args=progress_args
                        ),
                        video=raw.types.InputDocument(
                            id=uploaded_media.document.id,
                            access_hash=uploaded_media.document.access_hash,
                            file_reference=uploaded_media.document.file_reference,
                        ),
                        live_photo=True,
                        spoiler=self.has_spoiler,
                    ),
                )
            )

            media = raw.types.InputMediaPhoto(
                id=raw.types.InputPhoto(
                    id=uploaded_photo.photo.id,
                    access_hash=uploaded_photo.photo.access_hash,
                    file_reference=uploaded_photo.photo.file_reference,
                ),
                live_photo=True,
                spoiler=self.has_spoiler,
                video=raw.types.InputDocument(
                    id=uploaded_media.document.id,
                    access_hash=uploaded_media.document.access_hash,
                    file_reference=uploaded_media.document.file_reference,
                ),
            )
            return media, self.show_caption_above_media

        # file_id path: construct InputMediaPhoto with live_photo/video manually
        # (utils.get_input_media_from_file_id does not accept live_photo kwargs)
        try:
            photo_decoded = FileId.decode(self.photo)
        except Exception:
            if isinstance(self.photo, str) and re.match("^https?://", self.photo):
                raise ValueError(
                    "HTTP URLs are not supported for live photo file_id reconstruction"
                )
            raise ValueError(
                f'Failed to decode photo "{self.photo}". The value does not represent a valid file id.'
            )

        if photo_decoded.file_type != FileType.PHOTO:
            raise ValueError(
                f"Expected PHOTO, got {photo_decoded.file_type.name} file id instead"
            )

        try:
            video_decoded = FileId.decode(self.media)
        except Exception:
            raise ValueError(
                f'Failed to decode video "{self.media}". The value does not represent a valid file id.'
            )

        media = raw.types.InputMediaPhoto(
            id=raw.types.InputPhoto(
                id=photo_decoded.media_id,
                access_hash=photo_decoded.access_hash,
                file_reference=photo_decoded.file_reference,
            ),
            spoiler=self.has_spoiler,
            live_photo=True,
            video=raw.types.InputDocument(
                id=video_decoded.media_id,
                access_hash=video_decoded.access_hash,
                file_reference=video_decoded.file_reference,
            ),
        )
        return media, self.show_caption_above_media
