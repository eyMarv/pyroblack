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


class WebPagePreview(Object):
    """A web page preview.

    Parameters
    ----------
        webpage (:obj:`~pyrogram.types.WebPageEmpty` | :obj:`~pyrogram.types.WebPage`):
            Web Page Information.

        force_large_media (``bool``, *optional*):
            True, If the preview media size is forced to large.

        force_small_media  (``bool``, *optional*):
            True, If the preview media size is forced to small.

        is_safe (``bool``, *optional*):
            True, If the webpage is considered safe by telegram.

    """

    def __init__(
        self,
        *,
        webpage: types.WebPage | types.WebPageEmpty,
        force_large_media: bool | None = None,
        force_small_media: bool | None = None,
        invert_media: bool | None = None,
        is_safe: bool | None = None,
    ) -> None:
        super().__init__()

        self.webpage = webpage
        self.force_large_media = force_large_media
        self.force_small_media = force_small_media
        self.invert_media = invert_media
        self.is_safe = is_safe

    @staticmethod
    def _parse(
        client,
        web_page_preview: raw.types.WebPage | raw.types.WebPageEmpty,
        invert_media: bool | None = None,
    ):
        if isinstance(web_page_preview.webpage, raw.types.WebPage):
            webpage = types.WebPage._parse(client, web_page_preview.webpage)
        else:
            webpage = types.WebPageEmpty._parse(web_page_preview.webpage)
        return WebPagePreview(
            webpage=webpage,
            force_large_media=web_page_preview.force_large_media,
            force_small_media=web_page_preview.force_small_media,
            invert_media=invert_media,
            is_safe=web_page_preview.safe,
        )
