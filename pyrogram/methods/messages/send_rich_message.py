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

import logging
from typing import Optional, Union

import pyrogram
from pyrogram import raw, types, utils

log = logging.getLogger(__name__)


class SendRichMessage:
    async def send_rich_message(
        self: "pyrogram.Client",
        chat_id: Union[int, str],
        rich_message: "types.InputRichMessage",
        disable_notification: Optional[bool] = None,
        message_thread_id: Optional[int] = None,
        effect_id: Optional[int] = None,
        reply_parameters: Optional["types.ReplyParameters"] = None,
        protect_content: Optional[bool] = None,
        business_connection_id: Optional[str] = None,
        suggested_post_parameters: Optional["types.SuggestedPostParameters"] = None,
        reply_markup: Optional[
            Union[
                "types.InlineKeyboardMarkup",
                "types.ReplyKeyboardMarkup",
                "types.ReplyKeyboardRemove",
                "types.ForceReply",
            ]
        ] = None,
    ) -> "types.Message":
        """Send a rich text message.

        .. include:: /_includes/usable-by/bots.rst

        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target chat.

            rich_message (:obj:`~pyrogram.types.InputRichMessage`):
                The rich message content to send.

            disable_notification (``bool``, *optional*):
                Sends the message silently.

            message_thread_id (``int``, *optional*):
                Target message thread identifier for forum topics.

            effect_id (``int``, *optional*):
                Message effect identifier.

            reply_parameters (:obj:`~pyrogram.types.ReplyParameters`, *optional*):
                Reply parameters.

            protect_content (``bool``, *optional*):
                Protect from forwarding and saving.

            business_connection_id (``str``, *optional*):
                Business connection identifier.

            suggested_post_parameters (:obj:`~pyrogram.types.SuggestedPostParameters`, *optional*):
                Parameters for suggested posts.

            reply_markup (:obj:`~pyrogram.types.InlineKeyboardMarkup` | :obj:`~pyrogram.types.ReplyKeyboardMarkup` | :obj:`~pyrogram.types.ReplyKeyboardRemove` | :obj:`~pyrogram.types.ForceReply`, *optional*):
                Additional interface options.

        Returns:
            :obj:`~pyrogram.types.Message`: On success, the sent message is returned.
        """
        rpc = raw.functions.messages.SendMedia(
            peer=await self.resolve_peer(chat_id),
            media=raw.types.InputMediaRichMessage(
                rich_message=await rich_message.write(self),
            ),
            message="",
            random_id=self.rnd_id(),
            silent=disable_notification or None,
            noforwards=protect_content,
            effect=effect_id,
            reply_to=await utils._get_reply_message_parameters(
                self, message_thread_id, reply_parameters
            ),
            suggested_post=await suggested_post_parameters.write()
            if suggested_post_parameters
            else None,
            reply_markup=await reply_markup.write(self) if reply_markup else None,
        )

        if business_connection_id is not None:
            r = await self.invoke(
                raw.functions.InvokeWithBusinessConnection(
                    connection_id=business_connection_id, query=rpc
                )
            )
        else:
            r = await self.invoke(rpc, sleep_threshold=60)

        return await utils.parse_messages(self, r)
