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
from typing import Optional

from pyrogram import raw, types, utils

from ..object import Object


class SuggestedPostParameters(Object):
    """Contains parameters of a post that is being suggested.

    Parameters:
        price (:obj:`~pyrogram.types.SuggestedPostPrice`, *optional*):
            Proposed price for the post. If the field is omitted, then the post is unpaid.

        send_date (:py:obj:`~datetime.datetime`, *optional*):
            Proposed send date of the post.
            If specified, then the date must be between 300 second and 2678400 seconds (30 days) in the future.
            If the field is omitted, then the post can be published at any time within 30 days at the sole discretion of the user who approves it.
    """
    def __init__(
        self, *,
        price: Optional["types.SuggestedPostPrice"] = None,
        send_date: Optional[datetime] = None
    ):
        super().__init__()

        self.price = price
        self.send_date = send_date

    def write(self) -> "raw.types.SuggestedPost":
        return raw.types.SuggestedPost(
            price=self.price.write() if self.price else None,
            schedule_date=utils.datetime_to_timestamp(self.send_date)
        )
