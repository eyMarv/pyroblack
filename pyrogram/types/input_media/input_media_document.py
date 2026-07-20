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

import io
import os
import re
from typing import Callable

import pyrogram
from pyrogram import enums, raw, types, utils
from pyrogram.file_id import FileType

from .input_media import InputMedia


class InputMediaDocument(InputMedia):
    """A generic file to be sent inside an album.

    Parameters
    ----------
        media (``str`` | :obj:`io.BytesIO`):
            File to send.
            Pass a file_id as string to send a file that exists on the Telegram servers or
            pass a file path as string to upload a new file that exists on your local machine or
            pass a binary file-like object with its attribute “.name” set for in-memory uploads or
            pass an HTTP URL as a string for Telegram to get a file from the Internet.

        thumb (``str`` | :obj:`io.BytesIO`):
            Thumbnail of the file sent.
            The thumbnail should be in JPEG format and less than 200 KB in size.
            A thumbnail's width and height should not exceed 320 pixels.
            Thumbnails can't be reused and can be only uploaded as a new file.

        caption (``str``, *optional*):
            Caption of the document to be sent, 0-1024 characters.
            If not specified, the original caption is kept. Pass "" (empty string) to remove the caption.

        parse_mode (:obj:`~pyrogram.enums.ParseMode`, *optional*):
            By default, texts are parsed using both Markdown and HTML styles.
            You can combine both syntaxes together.

        caption_entities (List of :obj:`~pyrogram.types.MessageEntity`):
            List of special entities that appear in the caption, which can be specified instead of *parse_mode*.

        disable_content_type_detection (``bool``, *optional*):
            Pass True, if the uploaded video is a video message with no sound.
            Disables automatic server-side content type detection for files uploaded using multipart/form-data. Always True, if the document is sent as part of an album.

        file_name (``str``, *optional*):
            File name of the document sent.
            Defaults to file's path basename.

    """

    def __init__(
        self,
        media: str | io.BytesIO,
        thumb: str | io.BytesIO | None = None,
        caption: str = "",
        parse_mode: enums.ParseMode | None = None,
        caption_entities: list[types.MessageEntity] | None = None,
        disable_content_type_detection: bool | None = None,
        file_name: str | None = None,
    ) -> None:
        super().__init__(media, caption, parse_mode, caption_entities)

        self.thumb = thumb
        self.disable_content_type_detection = disable_content_type_detection
        self.file_name = file_name

    async def write(
        self,
        client: pyrogram.Client,
        chat_id: int | str | None = None,
        business_connection_id: str | None = None,
        progress: Callable | None = None,
        progress_args: tuple = (),
    ) -> tuple[
        InputMediaDocument | InputMediaDocumentExternal,
        bool,
    ]:
        is_bytes_io = isinstance(self.media, io.BytesIO)
        is_uploaded_file = is_bytes_io or os.path.isfile(self.media)
        is_external_url = not is_uploaded_file and re.match("^https?://", self.media)

        if is_bytes_io and not hasattr(self.media, "name"):
            self.media.name = self.file_name or "media"

        if is_uploaded_file:
            filename_attribute = [
                raw.types.DocumentAttributeFilename(
                    file_name=self.file_name
                    or (
                        self.media.name if is_bytes_io else os.path.basename(self.media)
                    ),
                ),
            ]
        else:
            filename_attribute = []

        if is_uploaded_file:
            media = await client.invoke(
                raw.functions.messages.UploadMedia(
                    business_connection_id=None,  # TODO
                    peer=await client.resolve_peer(chat_id or "me"),
                    media=raw.types.InputMediaUploadedDocument(
                        mime_type=(
                            None if is_bytes_io else client.guess_mime_type(self.media)
                        )
                        or "application/zip",
                        thumb=await client.save_file(self.thumb),
                        file=await client.save_file(self.media),
                        attributes=filename_attribute,
                        force_file=self.disable_content_type_detection,
                    ),
                ),
            )

            media = raw.types.InputMediaDocument(
                id=raw.types.InputDocument(
                    id=media.document.id,
                    access_hash=media.document.access_hash,
                    file_reference=media.document.file_reference,
                ),
            )
        elif is_external_url:
            media = raw.types.InputMediaDocumentExternal(
                url=self.media,
            )
        else:
            media = utils.get_input_media_from_file_id(self.media, FileType.DOCUMENT)

        return media, False
