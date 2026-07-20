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

import pyrogram
from pyrogram import raw, types

from .inline_query_result import InlineQueryResult

log = logging.getLogger(__name__)


class InlineQueryResultContact(InlineQueryResult):
    """Contact with a phone number.

    By default, this contact will be sent by the user.
    Alternatively, you can use *input_message_content* to send a message with the specified content instead of the
    contact.

    Parameters
    ----------
        phone_number (``str``):
            Phone number of the user.

        first_name (``str``):
            First name of the user; 1-64 characters.

        last_name (``str``, *optional*):
            Last name of the user; 0-64 characters.

        vcard (``str``, *optional*):
            Additional data about the user in a form of `vCard <https://en.wikipedia.org/wiki/VCard>`_; 0-2048 bytes in length.

        id (``str``, *optional*):
            Unique identifier for this result, 1-64 bytes.
            Defaults to a randomly generated UUID4.

        reply_markup (:obj:`~pyrogram.types.InlineKeyboardMarkup`, *optional*):
            Inline keyboard attached to the message.

        input_message_content (:obj:`~pyrogram.types.InputMessageContent`, *optional*):
            Content of the message to be sent instead of the contact.

        thumbnail_url (``str``, *optional*):
            Url of the thumbnail for the result.

        thumbnail_width (``int``, *optional*):
            Thumbnail width.

        thumbnail_height (``int``, *optional*):
            Thumbnail height.

    """

    def __init__(
        self,
        phone_number: str,
        first_name: str,
        last_name: str = "",
        vcard: str = "",
        id: str | None = None,
        reply_markup: types.InlineKeyboardMarkup = None,
        input_message_content: types.InputMessageContent = None,
        thumbnail_url: str | None = None,
        thumbnail_width: int = 0,
        thumbnail_height: int = 0,
        thumb_url: str | None = None,
        thumb_width: int | None = None,
        thumb_height: int | None = None,
    ) -> None:
        if thumb_url and thumbnail_url:
            msg = "Parameters `thumb_url` and `thumbnail_url` are mutually exclusive."
            raise ValueError(
                msg,
            )

        if thumb_url is not None:
            log.warning(
                "This property is deprecated. Please use thumbnail_url instead",
            )
            thumbnail_url = thumb_url

        if thumb_width and thumbnail_width:
            msg = (
                "Parameters `thumb_width` and `thumbnail_width` are mutually exclusive."
            )
            raise ValueError(
                msg,
            )

        if thumb_width is not None:
            log.warning(
                "This property is deprecated. Please use thumbnail_width instead",
            )
            thumbnail_width = thumb_width

        if thumb_height and thumbnail_height:
            msg = (
                "Parameters `thumb_height` and `thumbnail_height` are mutually "
                "exclusive."
            )
            raise ValueError(
                msg,
            )

        if thumb_height is not None:
            log.warning(
                "This property is deprecated. Please use thumbnail_height instead",
            )
            thumbnail_height = thumb_height

        super().__init__("contact", id, input_message_content, reply_markup)

        self.phone_number = phone_number
        self.first_name = first_name
        self.last_name = last_name
        self.vcard = vcard
        self.thumbnail_url = thumbnail_url
        self.thumb_url = thumbnail_url  # <=2.7.2
        self.thumbnail_width = thumbnail_width
        self.thumb_width = thumbnail_width  # <=2.7.2
        self.thumbnail_height = thumbnail_height
        self.thumb_height = thumbnail_height  # <=2.7.2

    async def write(self, client: pyrogram.Client):
        return raw.types.InputBotInlineResult(
            id=self.id,
            type=self.type,
            title=self.first_name,
            send_message=(
                await self.input_message_content.write(client, self.reply_markup)
                if self.input_message_content
                else raw.types.InputBotInlineMessageMediaContact(
                    phone_number=self.phone_number,
                    first_name=self.first_name,
                    last_name=self.last_name,
                    vcard=self.vcard,
                    reply_markup=await self.reply_markup.write(client)
                    if self.reply_markup
                    else None,
                )
            ),
            thumb=raw.types.InputWebDocument(
                url=self.thumbnail_url,
                size=0,
                mime_type="image/jpg",
                attributes=[
                    raw.types.DocumentAttributeImageSize(
                        w=self.thumbnail_width,
                        h=self.thumbnail_height,
                    ),
                ],
            )
            if self.thumbnail_url
            else None,
        )
