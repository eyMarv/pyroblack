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
from pyrogram import raw, types, utils
from pyrogram.types.object import Object
from pyrogram.types.update import Update


class ChatBoostUpdated(Object, Update):
    """A channel/supergroup boost has changed (bots only).

    Parameters
    ----------
        chat (:obj:`~pyrogram.types.Chat`):
            The chat where boost was changed.

        boost (:obj:`~pyrogram.types.ChatBoost`):
            New boost information.

    """

    def __init__(
        self,
        *,
        client: "pyrogram.Client" = None,
        chat: "types.Chat",
        boost: "types.ChatBoost",
    ) -> None:
        super().__init__(client)

        self.chat = chat
        self.boost = boost

    @staticmethod
    def _parse(
        client: "pyrogram.Client",
        update: "raw.types.UpdateBotChatBoost",
        users: dict[int, "raw.types.User"],
        chats: dict[int, "raw.types.Channel"],
    ) -> "ChatBoostUpdated":
        return ChatBoostUpdated(
            chat=types.Chat._parse_channel_chat(
                client, chats.get(utils.get_raw_peer_id(update.peer))
            ),
            boost=types.ChatBoost._parse(client, update.boost, users),
            client=client,
        )
