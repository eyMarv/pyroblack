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

import pyrogram
from pyrogram import raw, types
from pyrogram.types.object import Object


class InputPollOption(Object):
    """This object contains information about one answer option in a poll to send.

    Parameters
    ----------
        text (:obj:`~pyrogram.types.FormattedText`):
            Option text, 1-100 characters after entity parsing.
            Only custom emoji entities are allowed to be added and only by Premium users.

        media (:obj:`~pyrogram.types.InputMediaPhoto` | :obj:`~pyrogram.types.InputMediaVideo` | :obj:`~pyrogram.types.InputMediaSticker` | :obj:`~pyrogram.types.Location`, *optional*):
            Media associated with the option.
            Currently supports only photo, video, sticker or location.

    """

    def __init__(
        self,
        *,
        text: types.FormattedText,
        media: types.InputMediaPhoto
        | types.InputMediaVideo
        | types.InputMediaSticker
        | types.Location
        | None = None,
    ) -> None:
        super().__init__()

        self.text = text
        self.media = media

    async def write(
        self,
        client: pyrogram.Client,
    ) -> raw.types.PollAnswer:
        if isinstance(self.text, str):
            self.text = types.FormattedText(text=self.text)

        if self.media is not None and not isinstance(
            self.media,
            (
                types.InputMediaPhoto,
                types.InputMediaVideo,
                types.InputMediaSticker,
                types.Location,
            ),
        ):
            msg = f"Unsupported media type: {type(self.media)}"
            raise ValueError(msg)
        media = None
        if self.media:
            if isinstance(self.media, types.Location):
                media = await self.media.write()
            else:
                media, _ = await self.media.write(client=client)
        return raw.types.InputPollAnswer(
            text=await self.text.write(client),
            media=media,
        )
