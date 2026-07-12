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

from datetime import datetime

import pyrogram
from pyrogram import raw, types, utils

from ..object import Object


class BusinessIntro(Object):
    """

    Parameters:
        title (``str``, *optional*):
            Title text of the business intro
        
        message (``str``, *optional*):
            Message text of the business intro

        sticker (:obj:`~pyrogram.types.Sticker`, *optional*):
            Sticker of the business intro

    """

    def __init__(
        self,
        *,
        title: str = None,
        message: str = None,
        sticker: "types.Sticker" = None
    ):
        super().__init__()

        self.title = title
        self.message = message
        self.sticker = sticker


    @staticmethod
    async def _parse(
        client,
        business_intro: "raw.types.BusinessIntro"
    ) -> "BusinessIntro":
        doc = getattr(business_intro, "sticker", None)
        sticker = None
        if (
            doc and
            isinstance(doc, raw.types.Document)
        ):
            attributes = {type(i): i for i in doc.attributes}
            sticker = await types.Sticker._parse(
                client,
                doc,
                attributes
            )
        return BusinessIntro(
            title=getattr(business_intro, "title", None),
            message=getattr(business_intro, "description", None),
            sticker=sticker
        )
