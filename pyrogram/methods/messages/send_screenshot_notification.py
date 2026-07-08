#  pyroblack - Telegram MTProto API Client Library for Python
#  Copyright (C) 2022-present Mayuri-Chan <https://github.com/Mayuri-Chan>
#  Copyright (C) 2024-present eyMarv <https://github.com/eyMarv>
#
#  This file is part of pyroblack.
#
#  pyroblack is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Lesser General Public License as published
#  by the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  pyroblack is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public License
#  along with pyroblack.  If not, see <http://www.gnu.org/licenses/>.

from typing import Union

import pyrogram
from pyrogram import raw, types, utils


class SendScreenshotNotification:
    async def send_screenshot_notification(
        self: "pyrogram.Client",
        chat_id: Union[int, str],
        reply_parameters: "types.ReplyParameters" = None
    ) -> "types.Message":
        """Notify the other user in a private chat that a screenshot of the chat was taken.

        .. include:: /_includes/usable-by/users.rst

        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target chat.
                For your personal cloud (Saved Messages) you can simply use "me" or "self".
                For a contact that exists in your Telegram address book you can use his phone number (str).

            reply_parameters (:obj:`~pyrogram.types.ReplyParameters`, *optional*):
                Describes reply parameters for the message that is being sent.

        Returns:
            :obj:`~pyrogram.types.Message`: On success, the sent service message is returned.
        """

        r = await self.invoke(
            raw.functions.messages.SendScreenshotNotification(
                peer=await self.resolve_peer(chat_id),
                reply_to=await utils.get_reply_to(self, reply_parameters) if reply_parameters else raw.types.InputReplyToMessage(reply_to_msg_id=0),
                random_id=self.rnd_id()
            )
        )

        messages = await utils.parse_messages(client=self, messages=r)

        return messages[0] if messages else None
