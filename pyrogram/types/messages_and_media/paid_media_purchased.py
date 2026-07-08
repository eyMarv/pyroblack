#  Pyrogram - Telegram MTProto API Client Library for Python
#  Copyright (C) 2017-present Dan <https://github.com/delivrance>
#
#  This file is part of Pyrogram.
#
#  Pyrogram is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Lesser General Public License as published
#  by the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  Pyrogram is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public License
#  along with Pyrogram.  If not, see <http://www.gnu.org/licenses/>.

from pyrogram import types

from ..object import Object


class PaidMediaPurchased(Object):
    def __init__(self, *, from_user: "types.User" = None, paid_media_payload=None, _raw=None):
        super().__init__()
        self.from_user = from_user
        self.paid_media_payload = paid_media_payload
        self._raw = _raw

    @staticmethod
    def _parse(client, bot_purchased_paid_media, users) -> "PaidMediaPurchased":
        return PaidMediaPurchased(
            from_user=types.User._parse(client, users[bot_purchased_paid_media.user_id]),
            paid_media_payload=bot_purchased_paid_media.payload,
            _raw=bot_purchased_paid_media,
        )
