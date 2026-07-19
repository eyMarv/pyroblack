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

from typing import TYPE_CHECKING, Callable

from pyrogram.types.object import Object

if TYPE_CHECKING:
    import io

    from pyrogram import enums
    from pyrogram.types.messages_and_media import MessageEntity


class InputMedia(Object):
    """Content of a media message to be sent.

    It should be one of:

    - :obj:`~pyrogram.types.InputMediaAnimation`
    - :obj:`~pyrogram.types.InputMediaDocument`
    - :obj:`~pyrogram.types.InputMediaAudio`
    - :obj:`~pyrogram.types.InputMediaPhoto`
    - :obj:`~pyrogram.types.InputMediaVideo`
    """

    def __init__(
        self,
        media: str | io.BytesIO,
        caption: str | None = "",
        parse_mode: enums.ParseMode | None = None,
        caption_entities: list[MessageEntity] | None = None,
    ) -> None:
        super().__init__()

        self.media = media
        self.caption = caption
        self.parse_mode = parse_mode
        self.caption_entities = caption_entities

    async def write(
        self,
        client: pyrogram.Client,
        chat_id: int | str | None = None,
        business_connection_id: str | None = None,
        progress: Callable | None = None,
        progress_args: tuple = (),
    ) -> tuple[raw.base.InputMedia, bool]:
        raise NotImplementedError
