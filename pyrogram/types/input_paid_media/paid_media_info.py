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

import pyrogram
from pyrogram import raw, types
from ..object import Object


class PaidMediaInfo(Object):
    """Describes the paid media added to a message.

    Parameters:
        star_count (``int``):
            The number of Telegram Stars that must be paid to buy access to the media.

        paid_media  (List of :obj:`~pyrogram.types.PaidMedia`):
            Information about the paid media.

    """

    def __init__(
        self,
        *,
        star_count: str,
        paid_media: list["types.PaidMedia"]
    ):
        super().__init__()

        self.star_count = star_count
        self.paid_media = paid_media


    @staticmethod
    def _parse(
        client: "pyrogram.Client",
        message_paid_media: "raw.types.MessageMediaPaidMedia"
    ) -> "PaidMediaInfo":
        return PaidMediaInfo(
            star_count=message_paid_media.stars_amount,
            paid_media=[
                types.PaidMedia._parse(client, em)
                for em in message_paid_media.extended_media
            ]
        )
