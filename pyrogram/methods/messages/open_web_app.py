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

from typing import Optional, Union

import pyrogram
from pyrogram import enums, raw, types, utils


class OpenWebApp:
    async def open_web_app(
        self: "pyrogram.Client",
        chat_id: Union[int, str],
        bot_user_id: Union[int, str],
        url: Optional[str] = None,
        message_thread_id: Optional[int] = None,
        direct_messages_topic_id: Optional[int] = None,
        reply_parameters: Optional["types.ReplyParameters"] = None,
        platform: Optional["enums.ClientPlatform"] = None
    ) -> str:
        """Informs pyrogram that a Web App is being opened from the attachment menu,
        a :obj:`~pyrogram.types.MenuButton`, an url,
        or an :obj:`~pyrogram.types.InlineKeyboardButton` button.

        .. include:: /_includes/usable-by/users.rst

        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target chat.

            bot_user_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target bot.

            url (``str``, *optional*):
                The URL from an :obj:`~pyrogram.types.InlineKeyboardButton` or a :obj:`~pyrogram.types.MenuButton`.

            message_thread_id (``int``, *optional*):
                If not None, the message thread identifier to which the message will be sent.

            direct_messages_topic_id (``int``, *optional*):
                If not None, unique identifier of the topic of channel direct messages chat to which the message will be sent.

            reply_parameters (:obj:`~pyrogram.types.ReplyParameters`, *optional*):
                Information about the message or story to be replied in the message sent by the Web App.

            platform (:obj:`~pyrogram.enums.ClientPlatform`, *optional*):
                The platform on which the link will be opened.

        Returns:
            ``str``: On success, returns the url of a Web App.

        Example:
            .. code-block:: python

                link = await app.open_web_app(chat_id, bot_user_id)
        """
        if platform is None:
            platform = self.client_platform

        if direct_messages_topic_id is not None:
            if reply_parameters is None:
                reply_parameters = types.ReplyParameters(
                    direct_messages_topic_id=direct_messages_topic_id
                )
            elif getattr(reply_parameters, "direct_messages_topic_id", None) is None:
                reply_parameters.direct_messages_topic_id = direct_messages_topic_id

        r = await self.invoke(
            raw.functions.messages.RequestWebView(
                peer=await self.resolve_peer(chat_id),
                bot=await self.resolve_peer(bot_user_id),
                platform=platform.value,
                from_bot_menu=True if url is None else None,
                url=url,
                reply_to=await utils._get_reply_message_parameters(
                    self,
                    message_thread_id,
                    reply_parameters
                ),
            )
        )

        return r.url
