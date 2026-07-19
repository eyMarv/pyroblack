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

import logging
from typing import TYPE_CHECKING

import pyrogram
from pyrogram import enums, raw, types, utils

from .inline_session import get_session

if TYPE_CHECKING:
    from datetime import datetime

log = logging.getLogger(__name__)


class EditMessageText:
    async def edit_message_text(
        self: pyrogram.Client,
        chat_id: int | str,
        message_id: int,
        text: str,
        parse_mode: enums.ParseMode | None = None,
        entities: list[types.MessageEntity] | None = None,
        link_preview_options: types.LinkPreviewOptions = None,
        reply_markup: types.InlineKeyboardMarkup = None,
        schedule_date: datetime | None = None,
        business_connection_id: str | None = None,
        disable_web_page_preview: bool | None = None,
        **kwargs,
    ) -> types.Message:
        """Edit the text of messages.

        .. include:: /_includes/usable-by/users-bots.rst

        Parameters
        ----------
            chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target chat.
                For your personal cloud (Saved Messages) you can simply use "me" or "self".
                For a contact that exists in your Telegram address book you can use his phone number (str).

            message_id (``int``):
                Message identifier in the chat specified in chat_id.

            text (``str``):
                New text of the message.

            parse_mode (:obj:`~pyrogram.enums.ParseMode`, *optional*):
                By default, texts are parsed using both Markdown and HTML styles.
                You can combine both syntaxes together.

            entities (List of :obj:`~pyrogram.types.MessageEntity`):
                List of special entities that appear in message text, which can be specified instead of *parse_mode*.

            link_preview_options (:obj:`~pyrogram.types.LinkPreviewOptions`, *optional*):
                Link preview generation options for the message. Ignored if the specified URL does not have a valid preview.

            reply_markup (:obj:`~pyrogram.types.InlineKeyboardMarkup`, *optional*):
                An InlineKeyboardMarkup object.

            schedule_date (:py:obj:`~datetime.datetime`, *optional*):
                Date when the message will be automatically sent.

            business_connection_id (``str``, *optional*):
                Unique identifier of the business connection on behalf of which the message to be edited was sent

        Returns
        -------
            :obj:`~pyrogram.types.Message`: On success, the edited message is returned.

        Example:
            .. code-block:: python

                # Simple edit text
                await app.edit_message_text(chat_id, message_id, "new text")

                # Take the same text message, remove the web page preview only
                await app.edit_message_text(
                    chat_id, message_id, message.text,
                    link_preview_options=types.LinkPreviewOptions(
                        is_disabled=True
                    )
                )

        """
        if disable_web_page_preview and link_preview_options:
            msg = (
                "Parameters `disable_web_page_preview` and `link_preview_options` are mutually "
                "exclusive."
            )
            raise ValueError(
                msg,
            )

        if disable_web_page_preview is not None:
            log.warning(
                "This property is deprecated. Please use link_preview_options instead",
            )
            link_preview_options = types.LinkPreviewOptions(
                is_disabled=disable_web_page_preview
            )

        link_preview_options = link_preview_options or self.link_preview_options

        media = None
        if link_preview_options and link_preview_options.url:
            media = raw.types.InputMediaWebPage(
                url=link_preview_options.url,
                force_large_media=link_preview_options.prefer_large_media,
                force_small_media=link_preview_options.prefer_small_media,
                optional=True,
            )

        rpc = raw.functions.messages.EditMessage(
            peer=await self.resolve_peer(chat_id),
            id=message_id,
            no_webpage=link_preview_options.is_disabled
            if link_preview_options
            else None,
            invert_media=link_preview_options.show_above_text
            if link_preview_options
            else None,
            media=media,
            reply_markup=await reply_markup.write(self) if reply_markup else None,
            schedule_date=utils.datetime_to_timestamp(schedule_date),
            **await utils.parse_text_entities(self, text, parse_mode, entities),
        )
        session = None
        business_connection = None
        if business_connection_id:
            business_connection = self.business_user_connection_cache[
                business_connection_id
            ]
            if business_connection is None:
                business_connection = await self.get_business_connection(
                    business_connection_id
                )
            session = await get_session(
                self,
                business_connection._raw.connection.dc_id,
            )
        if business_connection_id:
            r = await session.invoke(
                raw.functions.InvokeWithBusinessConnection(
                    query=rpc,
                    connection_id=business_connection_id,
                ),
            )
            # await session.stop()
        else:
            r = await self.invoke(rpc)

        for i in r.updates:
            if isinstance(
                i,
                (
                    raw.types.UpdateEditMessage,
                    raw.types.UpdateEditChannelMessage,
                    raw.types.UpdateNewScheduledMessage,
                ),
            ):
                return await types.Message._parse(
                    self,
                    i.message,
                    {i.id: i for i in r.users},
                    {i.id: i for i in r.chats},
                    is_scheduled=isinstance(i, raw.types.UpdateNewScheduledMessage),
                    replies=self.fetch_replies,
                )
            if isinstance(
                i,
                (raw.types.UpdateBotEditBusinessMessage),
            ):
                return await types.Message._parse(
                    self,
                    i.message,
                    {i.id: i for i in r.users},
                    {i.id: i for i in r.chats},
                    business_connection_id=getattr(
                        i, "connection_id", business_connection_id
                    ),
                    raw_reply_to_message=i.reply_to_message,
                    replies=0,
                )
        return None
