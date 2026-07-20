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

from typing import TYPE_CHECKING

from pyrogram import enums, raw, types, utils
from pyrogram.types.object import Object

if TYPE_CHECKING:
    from datetime import datetime


class SuggestedPostInfo(Object):
    """Contains information about a suggested post.

    Parameters
    ----------
        price (:obj:`~pyrogram.types.SuggestedPostPrice`, *optional*):
            Proposed price of the post.
            If the field is omitted, then the post is unpaid.

        send_date (:py:obj:`~datetime.datetime`, *optional*):
            Proposed send date of the post.
            If the field is omitted, then the post can be published at any time
            within 30 days at the sole discretion of the user or administrator who approves it.

        state (:obj:`~pyrogram.enums.SuggestedPostState`, *optional*):
            State of the suggested post.

    """

    def __init__(
        self,
        *,
        price: types.SuggestedPostPrice | None = None,
        send_date: datetime | None = None,
        state: enums.SuggestedPostState | None = None,
    ) -> None:
        super().__init__()

        self.price = price
        self.send_date = send_date
        self.state = state

    @staticmethod
    def _parse(suggested_post: raw.types.SuggestedPost) -> SuggestedPostInfo | None:
        if not suggested_post:
            return None

        state = None

        if suggested_post.accepted:
            state = enums.SuggestedPostState.APPROVED
        elif suggested_post.rejected:
            state = enums.SuggestedPostState.DECLINED
        else:
            state = enums.SuggestedPostState.PENDING

        return SuggestedPostInfo(
            price=types.SuggestedPostPrice._parse(suggested_post.price),
            send_date=utils.timestamp_to_datetime(suggested_post.schedule_date),
            state=state,
        )
