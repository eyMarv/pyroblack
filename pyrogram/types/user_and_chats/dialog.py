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

import pyrogram
from pyrogram import raw
from pyrogram import types
from ..object import Object
from ... import utils


class Dialog(Object):
    """A user's dialog.

    Parameters:
        chat (:obj:`~pyrogram.types.Chat`):
            Conversation the dialog belongs to.

        top_message (:obj:`~pyrogram.types.Message`):
            The last message sent in the dialog at this time.

        unread_messages_count (``int``):
            Amount of unread messages in this dialog.

        unread_mentions_count (``int``):
            Amount of unread messages containing a mention in this dialog.

        unread_reactions_count (``int``):
            Amount of unread messages containing a reaction in this dialog.

        unread_mark (``bool``):
            True, if the dialog has the unread mark set.

        is_pinned (``bool``):
            True, if the dialog is pinned.

        folder_id (``int``, *optional*):
            Unique identifier (int) of the folder.

        ttl_period (``int``, *optional*)
            Time-to-live of all messages sent in this dialog (in seconds).

        raw (:obj:`~pyrogram.raw.functions.Dialog`, *optional*):
            The raw object, as received from the Telegram API.
    """

    def __init__(
        self,
        *,
        client: "pyrogram.Client" = None,
        chat: "types.Chat",
        top_message: "types.Message",
        unread_messages_count: int,
        unread_mentions_count: int,
        unread_reactions_count: int,
        unread_mark: bool,
        is_pinned: bool,
        folder_id: int = None,
        ttl_period: int = None,
        raw: "raw.functions.Dialog" = None,
    ):
        super().__init__(client)

        self.chat = chat
        self.top_message = top_message
        self.unread_messages_count = unread_messages_count
        self.unread_mentions_count = unread_mentions_count
        self.unread_reactions_count = unread_reactions_count
        self.unread_mark = unread_mark
        self.is_pinned = is_pinned
        self.folder_id = folder_id
        self.ttl_period = ttl_period
        self.raw = raw

    @staticmethod
    def _parse(client, dialog: "raw.functions.Dialog", messages, users, chats) -> "Dialog":
        return Dialog(
            chat=types.Chat._parse_dialog(client, dialog.peer, users, chats),
            top_message=messages.get(utils.get_peer_id(dialog.peer)),
            unread_messages_count=dialog.unread_count,
            unread_mentions_count=dialog.unread_mentions_count,
            unread_reactions_count=dialog.unread_reactions_count,
            unread_mark=dialog.unread_mark,
            is_pinned=dialog.pinned,
            folder_id=getattr(dialog, "folder_id", None),
            ttl_period=getattr(dialog, "ttl_period", None),
            raw=dialog,
            client=client,
        )
