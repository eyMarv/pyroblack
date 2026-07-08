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

import asyncio
import io
import os
import re
from datetime import datetime
from typing import Union, Optional, Callable, BinaryIO

import pyrogram
from pyrogram import types, utils
from pyrogram.file_id import FileId, FileType, PHOTO_TYPES

DEFAULT_DOWNLOAD_DIR = "downloads/"


class DownloadMedia:
    async def download_media(
        self: "pyrogram.Client",
        message: Union[
            "types.Message",
            "types.Story",
            "types.PaidMediaInfo",
            "types.PaidMediaPhoto",
            "types.PaidMediaVideo",
            "types.PaidMediaPreview",
            "types.Thumbnail",
            "types.StrippedThumbnail",
            str,
        ],
        file_name: str = DEFAULT_DOWNLOAD_DIR,
        in_memory: bool = False,
        block: bool = True,
        idx: int = None,
        progress: Callable = None,
        progress_args: tuple = (),
    ) -> Optional[Union[str, BinaryIO, list[str], list["io.BytesIO"]]]:
        """Download the media from a message.

        .. include:: /_includes/usable-by/users-bots.rst

        Parameters:
            message (:obj:`~pyrogram.types.Message` | :obj:`~pyrogram.types.Story` | ``str``):
                Pass a Message/Story containing the media, the media itself (message.audio, message.video, ...) or a file id
                as string.

            file_name (``str``, *optional*):
                A custom *file_name* to be used instead of the one provided by Telegram.
                By default, all files are downloaded in the *downloads* folder in your working directory.
                You can also specify a path for downloading files in a custom location: paths that end with "/"
                are considered directories. All non-existent folders will be created automatically.

            in_memory (``bool``, *optional*):
                Pass True to download the media in-memory.
                A binary file-like object with its attribute ".name" set will be returned.
                Defaults to False.

            block (``bool``, *optional*):
                Blocks the code execution until the file has been downloaded.
                Defaults to True.

            progress (``Callable``, *optional*):
                Pass a callback function to view the file transmission progress.
                The function must take *(current, total)* as positional arguments (look at Other Parameters below for a
                detailed description) and will be called back each time a new file chunk has been successfully
                transmitted.

            progress_args (``tuple``, *optional*):
                Extra custom arguments for the progress callback function.
                You can pass anything you need to be available in the progress callback scope; for example, a Message
                object or a Client instance in order to edit the message with the updated progress status.

        Other Parameters:
            current (``int``):
                The amount of bytes transmitted so far.

            total (``int``):
                The total size of the file.

            *args (``tuple``, *optional*):
                Extra custom arguments as defined in the ``progress_args`` parameter.
                You can either keep ``*args`` or add every single extra argument in your function signature.

        Returns:
            ``str`` | ``None`` | ``BinaryIO``: On success, the absolute path of the downloaded file is returned,
            otherwise, in case the download failed or was deliberately stopped with
            :meth:`~pyrogram.Client.stop_transmission`, None is returned.
            Otherwise, in case ``in_memory=True``, a binary file-like object with its attribute ".name" set is returned.

        Raises:
            ValueError: if the message doesn't contain any downloadable media

        Example:
            Download media to file

            .. code-block:: python

                # Download from Message
                await app.download_media(message)

                # Download from file id
                await app.download_media(message.photo.file_id)

                # Download document of a message
                await app.download_media(message.document)

                # Keep track of the progress while downloading
                async def progress(current, total):
                    print(f"{current * 100 / total:.1f}%")

                await app.download_media(message, progress=progress)

            Download media in-memory

            .. code-block:: python

                file = await app.download_media(message, in_memory=True)

                file_name = file.name
                file_bytes = bytes(file.getbuffer())
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

        media_items = [message]

        if isinstance(message, types.Message):
            if message.new_chat_photo:
                media_items = [message.new_chat_photo]
            elif message.paid_media:
                media_items = []
                for paid_media in message.paid_media.paid_media:
                    if isinstance(paid_media, types.PaidMediaPhoto):
                        media_items.append(paid_media.photo)
                    elif isinstance(paid_media, types.PaidMediaVideo):
                        media_items.append(paid_media.video)
                    elif isinstance(paid_media, types.PaidMediaPreview) and paid_media.minithumbnail:
                        media_items.append(paid_media.minithumbnail.data)
            else:
                media_items = []
                for kind in available_media:
                    media = getattr(message, kind, None)
                    if media is not None:
                        media_items = [media]
                        break
        elif isinstance(message, types.Story):
            media_items = []
            for kind in ("photo", "video"):
                media = getattr(message, kind, None)
                if media is not None:
                    media_items = [media]
                    break
        elif isinstance(message, types.PaidMediaInfo):
            media_items = []
            for paid_media in message.paid_media:
                if isinstance(paid_media, types.PaidMediaPhoto):
                    media_items.append(paid_media.photo)
                elif isinstance(paid_media, types.PaidMediaVideo):
                    media_items.append(paid_media.video)
                elif isinstance(paid_media, types.PaidMediaPreview) and paid_media.minithumbnail:
                    media_items.append(paid_media.minithumbnail.data)
        elif isinstance(message, types.PaidMediaPhoto):
            media_items = [message.photo]
        elif isinstance(message, types.PaidMediaVideo):
            media_items = [message.video]
        elif isinstance(message, types.PaidMediaPreview):
            media_items = [message.minithumbnail.data] if message.minithumbnail else []
        elif isinstance(message, types.StrippedThumbnail):
            media_items = [message.data]
        elif isinstance(message, types.Thumbnail):
            media_items = [message]
        elif hasattr(message, "file_id"):
            media_items = [message]
        else:
            media_items = [message]

        media_items = types.List(filter(lambda item: item is not None, media_items))

        if not media_items:
            if isinstance(message, str):
                media_items = [message]
            else:
                raise ValueError("This message doesn't contain any downloadable media")

        if idx is not None:
            media_items = [media_items[idx]]

        downloads = []

        for media in media_items:
            if isinstance(media, bytes):
                thumbnail = utils.from_inline_bytes(
                    utils.expand_inline_bytes(media)
                )

                if in_memory:
                    downloads.append(thumbnail)
                    continue

                directory, current_file_name = os.path.split(file_name)
                current_file_name = current_file_name or thumbnail.name

                if not os.path.isabs(current_file_name):
                    directory = self.PARENT_DIR / (directory or DEFAULT_DOWNLOAD_DIR)

                os.makedirs(directory, exist_ok=True)
                absolute_path = os.path.abspath(
                    re.sub("\\\\", "/", os.path.join(directory, current_file_name))
                )

                with open(absolute_path, "wb") as file:
                    file.write(thumbnail.getbuffer())

                downloads.append(absolute_path)
                continue

            if isinstance(media, str):
                file_id_str = media
            else:
                file_id_str = media.file_id

            file_id_obj = FileId.decode(file_id_str)
            file_type = file_id_obj.file_type
            media_file_name = getattr(media, "file_name", "")
            file_size = getattr(media, "file_size", 0)
            mime_type = getattr(media, "mime_type", "")
            date = getattr(media, "date", None)

            directory, current_file_name = os.path.split(file_name)
            current_file_name = current_file_name or media_file_name or ""

            if not os.path.isabs(current_file_name):
                directory = self.PARENT_DIR / (directory or DEFAULT_DOWNLOAD_DIR)

            if not current_file_name:
                guessed_extension = self.guess_extension(mime_type)

                if file_type in PHOTO_TYPES:
                    extension = ".jpg"
                elif file_type == FileType.VOICE:
                    extension = guessed_extension or ".ogg"
                elif file_type in (FileType.VIDEO, FileType.ANIMATION, FileType.VIDEO_NOTE):
                    extension = guessed_extension or ".mp4"
                elif file_type == FileType.DOCUMENT:
                    extension = guessed_extension or ".zip"
                elif file_type == FileType.STICKER:
                    extension = guessed_extension or ".webp"
                elif file_type == FileType.AUDIO:
                    extension = guessed_extension or ".mp3"
                else:
                    extension = ".unknown"

                current_file_name = "{}_{}_{}{}".format(
                    FileType(file_id_obj.file_type).name.lower(),
                    (date or datetime.now()).strftime("%Y-%m-%d_%H-%M-%S"),
                    self.rnd_id(),
                    extension,
                )

            downloader = self.handle_download(
                (
                    file_id_obj,
                    directory,
                    current_file_name,
                    in_memory,
                    file_size,
                    progress,
                    progress_args,
                )
            )

            if block:
                downloads.append(await downloader)
            else:
                self.loop.create_task(downloader)

        if not block:
            return None

        if len(downloads) == 1:
            return downloads[0]

        return types.List(downloads)
