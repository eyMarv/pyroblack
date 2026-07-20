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
from pyrogram import raw
from pyrogram.types.object import Object


class DirectMessagePriceChanged(Object):
    """Describes a service message about a change in the price of direct messages sent to a channel chat.

    Parameters
    ----------
        are_direct_messages_enabled (``bool``):
            True, if direct messages are enabled for the channel chat; False otherwise.

        direct_message_star_count (``int``, *optional*):
            The new number of Telegram Stars that must be paid by users for each direct message sent to the channel. Does not apply to users who have been exempted by administrators. Defaults to 0.

    """

    def __init__(
        self,
        *,
        client: pyrogram.Client = None,
        are_direct_messages_enabled: bool | None = None,
        direct_message_star_count: int = 0,
    ) -> None:
        super().__init__(client)

        self.are_direct_messages_enabled = are_direct_messages_enabled
        self.direct_message_star_count = direct_message_star_count

    @staticmethod
    def _parse_action(
        client,
        action: raw.types.MessageActionPaidMessagesPrice,
    ) -> DirectMessagePriceChanged:
        if isinstance(action, raw.types.MessageActionPaidMessagesPrice):
            return DirectMessagePriceChanged(
                client=client,
                are_direct_messages_enabled=True,  # action.broadcast_messages_allowed,
                direct_message_star_count=action.stars,
            )
        return None
