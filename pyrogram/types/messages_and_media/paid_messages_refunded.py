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


class PaidMessagesRefunded(Object):
    """Describes a service message about refunded paid messages.

    Parameters:
        message_count (``int``):
            The number of refunded messages.

        star_count (``int``):
            The number of refunded Telegram Stars.

    """

    def __init__(
        self,
        *,
        client: "pyrogram.Client" = None,
        message_count: int = None,
        star_count: int = None
    ):
        super().__init__(client)

        self.message_count = message_count
        self.star_count = star_count


    @staticmethod
    def _parse_action(
        client,
        action: "raw.types.MessageActionPaidMessagesRefunded"
    ) -> "PaidMessagesRefunded":
        if isinstance(action, raw.types.MessageActionPaidMessagesRefunded):
            return PaidMessagesRefunded(
                client=client,
                message_count=action.count,
                star_count=action.stars
            )
