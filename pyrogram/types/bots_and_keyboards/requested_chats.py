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

from typing import List, Union

import pyrogram

from ..object import Object
from pyrogram import raw, types, utils, enums
from typing import Union, List


class RequestedChats(Object):
    """Contains information about requested chats.

    Parameters:
        button_id (``int``):
            Identifier of button.

        chats (List of :obj:`~pyrogram.types.Chat`):
            List of requested chats.
    """

    def __init__(
        self,
        *,
        client: "pyrogram.Client" = None,
        button_id: int,
        chats: List["types.Chat"],
    ):
        super().__init__(client)

        self.button_id = button_id
        self.chats = chats

    @staticmethod
    def _parse(
        client,
        action: Union[
            "raw.types.MessageActionRequestedPeer",
            "raw.types.MessageActionRequestedPeerSentMe",
        ],
    ) -> "RequestedChats":
        _requested_chats = []

        for requested_peer in action.peers:
            peer_id = utils.get_peer_id(requested_peer)
            peer_type = utils.get_peer_type(peer_id)

            if peer_type == "user":
                chat_type = enums.ChatType.PRIVATE
            elif peer_type == "chat":
                chat_type = enums.ChatType.GROUP
            else:
                chat_type = enums.ChatType.CHANNEL

            _requested_chats.append(
                types.Chat(
                    id=peer_id,
                    type=chat_type,
                    first_name=getattr(requested_peer, "first_name", None),
                    last_name=getattr(requested_peer, "last_name", None),
                    username=getattr(requested_peer, "username", None),
                    photo=types.ChatPhoto._parse(
                        client, getattr(requested_peer, "photo", None), peer_id, 0
                    ),
                    client=client,
                )
            )

        return RequestedChats(
            button_id=action.button_id,
            chats=types.List(_requested_chats),
            client=client,
        )
