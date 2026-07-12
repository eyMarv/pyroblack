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


class PaidMessagePriceChanged(Object):
    """Describes a service message about a change in the price of paid messages within a chat.

    Parameters:
        paid_message_star_count (``int``):
            The new number of Telegram Stars that must be paid by non-administrator users of the supergroup chat for each sent message.

    """

    def __init__(
        self,
        *,
        client: "pyrogram.Client" = None,
        paid_message_star_count: int = None
    ):
        super().__init__(client)

        self.paid_message_star_count = paid_message_star_count


    @staticmethod
    def _parse_action(
        client,
        action: "raw.types.MessageActionPaidMessagesPrice"
    ) -> "PaidMessagePriceChanged":
        if isinstance(action, raw.types.MessageActionPaidMessagesPrice):
            return PaidMessagePriceChanged(
                client=client,
                paid_message_star_count=action.stars
            )
