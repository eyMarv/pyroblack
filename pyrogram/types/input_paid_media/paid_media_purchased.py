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


class PaidMediaPurchased(Object):
    """This object contains information about a paid media purchase.

    Parameters
    ----------
        from_user (:obj:`~pyrogram.types.User`):
            User who purchased the media.

        paid_media_payload (``str``):
            Bot-specified paid media payload.

    """

    def __init__(
        self,
        from_user: types.User = None,
        paid_media_payload: str | None = None,
        _raw: raw.types.UpdateBotPurchasedPaidMedia = None,
    ) -> None:
        super().__init__()

        self.from_user = from_user
        self.paid_media_payload = paid_media_payload
        self._raw = _raw

    @staticmethod
    def _parse(
        client: pyrogram.Client,
        bot_purchased_paid_media: raw.types.UpdateBotPurchasedPaidMedia,
        users: dict,
    ) -> PaidMediaPurchased:
        return PaidMediaPurchased(
            from_user=types.User._parse(
                client, users[bot_purchased_paid_media.user_id]
            ),
            paid_media_payload=bot_purchased_paid_media.payload,
            _raw=bot_purchased_paid_media,
        )
