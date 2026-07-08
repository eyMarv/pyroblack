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

from typing import Optional, Union

import pyrogram
from pyrogram import raw, types


class SendRichMessageDraft:
    async def send_rich_message_draft(
        self: "pyrogram.Client",
        chat_id: Union[int, str],
        draft_id: int,
        rich_message: "types.InputRichMessage",
        message_thread_id: Optional[int] = None,
    ) -> bool:
        """Stream a partial rich message to a user while the message is being generated.

        .. note::

            The streamed draft is ephemeral and acts as a temporary preview — once the output
            is finalized, call :meth:`~pyrogram.Client.send_rich_message` with the complete message
            to persist it in the user's chat.

        .. include:: /_includes/usable-by/bots.rst

        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target chat.

            draft_id (``int``):
                Unique identifier of the message draft, must be non-zero.
                Changes to drafts with the same identifier are animated.

            rich_message (:obj:`pyrogram.types.InputRichMessage`):
                The partial message to be streamed.

            message_thread_id (``int``, *optional*):
                Unique identifier for the target message thread.

        Returns:
            ``bool``: On success, True is returned.
        """
        return bool(
            await self.invoke(
                raw.functions.messages.SetTyping(
                    peer=await self.resolve_peer(chat_id),
                    action=raw.types.SendMessageRichMessageDraftAction(
                        random_id=draft_id,
                        rich_message=await rich_message.write(self),
                    ),
                    top_msg_id=message_thread_id,
                )
            )
        )
