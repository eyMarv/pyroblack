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

from pyrogram import raw, types
from pyrogram.types.object import Object


class PaidMedia(Object):
    """A PaidMedia.

    Parameters
    ----------
        stars_amount (``int``):
            Amount of stars.

        extended_media (List of :obj:`~pyrogram.types.Animation` | :obj:`~pyrogram.types.ExtendedMediaPreview` | :obj:`~pyrogram.types.Photo` | :obj:`~pyrogram.types.Video`, *optional*):
            Extended media.

    """

    def __init__(
        self,
        *,
        stars_amount: int,
        extended_media: list[
            types.Animation | types.ExtendedMediaPreview | types.Photo | types.Video
        ]
        | None = None,
    ) -> None:
        super().__init__()

        self.stars_amount = stars_amount
        self.extended_media = extended_media

    @staticmethod
    def _parse(client, media: raw.types.MessageMediaPaidMedia) -> PaidMedia:
        extended_media = []
        for m in media.extended_media:
            if isinstance(m, raw.types.MessageExtendedMediaPreview):
                extended_media.append(types.ExtendedMediaPreview._parse(client, m))
            elif isinstance(m.media, raw.types.MessageMediaPhoto):
                extended_media.append(
                    types.Photo._parse(client, m.media.photo, m.media.ttl_seconds),
                )
            elif isinstance(m.media, raw.types.MessageMediaDocument):
                attributes = {type(i): i for i in m.media.document.attributes}
                file_name = getattr(
                    attributes.get(raw.types.DocumentAttributeFilename),
                    "file_name",
                    None,
                )
                if raw.types.DocumentAttributeAnimated in attributes:
                    video_attributes = attributes.get(raw.types.DocumentAttributeVideo)
                    extended_media.append(
                        types.Animation._parse(
                            client,
                            m.media.document,
                            video_attributes,
                            file_name,
                        ),
                    )
                else:
                    video_attributes = attributes[raw.types.DocumentAttributeVideo]
                    extended_media.append(
                        types.Video._parse(
                            client,
                            m.media.document,
                            video_attributes,
                            file_name,
                            m.media.ttl_seconds,
                        ),
                    )
        return PaidMedia(stars_amount=media.stars_amount, extended_media=extended_media)
