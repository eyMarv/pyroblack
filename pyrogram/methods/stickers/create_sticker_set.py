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

import os
import re

import pyrogram
from pyrogram import raw, types, utils
from pyrogram.file_id import FileId, FileType


class CreateStickerSet:
    async def create_sticker_set(
        self: pyrogram.Client,
        title: str,
        short_name: str,
        sticker: str,
        user_id: int | str | None = None,
        emoji: str = "🤔",
        masks: bool | None = None,
        animated: bool | None = None,
        videos: bool | None = None,
        emojis: bool | None = None,
    ) -> types.Message | None:
        """Create a new stickerset.

        .. include:: /_includes/usable-by/users-bots.rst

        Parameters
        ----------
            title (``str``):
                Stickerset name, 1-64 chars

            short_name (``str``, *optional*):
                Short name of sticker set, to be used in sticker deep links.
                Can contain only english letters, digits and underscores.
                Must begin with a letter, can't contain consecutive underscores and, if called by a bot, must end in "_by_<bot_username>".
                <bot_username> is case insensitive. 1-64 characters.

            sticker (``str``):
                sticker to add.
                Pass a file_id as string to send a file that exists on the Telegram servers.

            user_id (``int`` | ``str``, *optional*):
                Unique identifier (int) or username (str) of the Stickerset owner.
                For you yourself you can simply use "me" or "self" (users only).
                required for bots.
                default to "me".

            emoji (``str``, *optional*):
                Associated emoji.
                default to "🤔"

            masks (``bool``, *optional*):
                Whether this is a mask stickerset.

            animated (``bool``, *optional*):
                Whether this is a animated stickerset.

            videos (``bool``, *optional*):
                Whether this is a videos stickerset.

            emojis (``bool``, *optional*):
                Whether this is a emojis stickerset.

        Returns
        -------
            :obj:`~pyrogram.types.StickerSet` | ``None``: On success, the StickerSet is returned.

        Example:
            .. code-block:: python

                await app.create_sticker_set("me", "My First Pack", "myfirstpack", "AAjjHjk")

        """
        if self.me.is_bot and user_id is None:
            msg = "user_id is required for bots"
            raise ValueError(msg)

        if isinstance(sticker, str):
            if os.path.isfile(sticker) or re.match("^https?://", sticker):
                document = await self.send_document(
                    user_id or "me",
                    sticker,
                    force_document=True,
                    disable_notification=True,
                )
                uploaded_media = utils.get_input_media_from_file_id(
                    document.document.file_id,
                    FileType.DOCUMENT,
                )
                media = uploaded_media.id
                _ = await document.delete()
            else:
                decoded = FileId.decode(sticker)
                media = raw.types.InputDocument(
                    id=decoded.media_id,
                    access_hash=decoded.access_hash,
                    file_reference=decoded.file_reference,
                )
        else:
            document = await self.send_document(
                user_id or "me",
                sticker,
                force_document=True,
                disable_notification=True,
            )
            uploaded_media = utils.get_input_media_from_file_id(
                document.document.file_id,
                FileType.DOCUMENT,
            )
            media = uploaded_media.id
            _ = await document.delete()

        r = await self.invoke(
            raw.functions.stickers.CreateStickerSet(
                user_id=await self.resolve_peer(user_id or "me"),
                title=title,
                short_name=short_name,
                stickers=[raw.types.InputStickerSetItem(document=media, emoji=emoji)],
                masks=masks,
                animated=animated,
                videos=videos,
                emojis=emojis,
            ),
        )

        return types.StickerSet._parse(r.set)
