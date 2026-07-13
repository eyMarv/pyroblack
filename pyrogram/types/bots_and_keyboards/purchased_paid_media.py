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

from pyrogram import raw, types

from ..object import Object


class PurchasedPaidMedia(Object):
    """This object represents information about purchased paid media.

    Parameters:
        from_user (:obj:`~pyrogram.types.User`):
            User who bought the paid media.

        payload (``str``):
            Bot-defined invoice payload, 1-128 bytes. This will not be displayed to the user, use for your internal processes.
    """

    def __init__(
        self,
        from_user: "types.User",
        payload: str
    ):
        super().__init__()

        self.from_user = from_user
        self.payload = payload

    @staticmethod
    def _parse(client, purchased_media: "raw.types.UpdateBotPurchasedPaidMedia", users) -> "PurchasedPaidMedia":
        return PurchasedPaidMedia(
            from_user=types.User._parse(client, users.get(purchased_media.user_id)),
            payload=purchased_media.payload
        )
