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

from typing import Optional

import pyrogram
from pyrogram import raw, types, utils
from pyrogram.types.object import Object


class FoundContacts(Object):
    """Chats found by name substring and auxiliary data.

    Parameters
    ----------
        my_results (List of :obj:`~pyrogram.types.Chat`, *optional*):
            Personalized results.

        global_results (List of :obj:`~pyrogram.types.Chat`, *optional*):
            List of found chats in global search.

    """

    def __init__(
        self,
        *,
        client: "pyrogram.Client" = None,
        my_results: Optional["types.Chat"] = None,
        global_results: Optional["types.Chat"] = None,
    ) -> None:
        super().__init__(client)

        self.my_results = my_results
        self.global_results = global_results

    @staticmethod
    def _parse(client, found: "raw.types.contacts.Found") -> "FoundContacts":
        users = {u.id: u for u in found.users}
        chats = {c.id: c for c in found.chats}

        my_results = []
        global_results = []

        for result in found.my_results:
            peer_id = utils.get_raw_peer_id(result)
            peer = users.get(peer_id) or chats.get(peer_id)

            my_results.append(types.Chat._parse_chat(client, peer))

        for result in found.results:
            peer_id = utils.get_raw_peer_id(result)
            peer = users.get(peer_id) or chats.get(peer_id)

            global_results.append(types.Chat._parse_chat(client, peer))

        return FoundContacts(
            my_results=types.List(my_results) or None,
            global_results=types.List(global_results) or None,
            client=client,
        )
