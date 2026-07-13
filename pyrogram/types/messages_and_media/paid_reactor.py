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

from typing import Dict, Optional

import pyrogram
from pyrogram import raw, types, utils

from ..object import Object


class PaidReactor(Object):
    """Contains information about a user that added paid reactions.

    Parameters:
        sender (:obj:`~pyrogram.types.Chat`, *optional*):
            Identifier of the user or chat that added the reactions.
            May be None for anonymous reactors that aren't the current user

        star_count (``int``, *optional*):
            True, if the reactions are tags and Telegram Premium users can filter messages by them.

        is_top (``bool``, *optional*):
            True, if the reactor is one of the most active reactors.
            May be False if the reactor is the current user.

        is_me (``bool``, *optional*):
            True, if the paid reaction was added by the current user.

        is_anonymous (``bool``, *optional*):
            True, if the reactor is anonymous.
    """

    def __init__(
        self,
        *,
        sender: Optional["types.Chat"] = None,
        star_count: Optional[int] = None,
        is_top: Optional[bool] = None,
        is_me: Optional[bool] = None,
        is_anonymous: Optional[bool] = None,
    ):
        super().__init__()

        self.sender = sender
        self.star_count = star_count
        self.is_top = is_top
        self.is_me = is_me
        self.is_anonymous = is_anonymous

    @staticmethod
    def _parse(
        client: "pyrogram.Client",
        paid_reactor: Optional["raw.base.MessageReactor"],
        users: Dict[int, "raw.base.User"],
        chats: Dict[int, "raw.base.Chat"],
    ) -> Optional["PaidReactor"]:
        if not paid_reactor:
            return None

        chat = chats.get(utils.get_raw_peer_id(paid_reactor.peer_id)) or users.get(
            utils.get_raw_peer_id(paid_reactor.peer_id)
        )

        return PaidReactor(
            sender=types.Chat._parse_chat(client, chat),
            star_count=paid_reactor.count,
            is_top=paid_reactor.top,
            is_me=paid_reactor.my,
            is_anonymous=paid_reactor.anonymous,
        )
