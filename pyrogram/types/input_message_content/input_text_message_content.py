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
from pyrogram import enums, raw, types, utils

from .input_message_content import InputMessageContent

log = logging.getLogger(__name__)


class InputTextMessageContent(InputMessageContent):
    """Content of a text message to be sent as the result of an inline query.

    Parameters
    ----------
        message_text (``str``):
            Text of the message to be sent, 1-4096 characters.

        parse_mode (:obj:`~pyrogram.enums.ParseMode`, *optional*):
            By default, texts are parsed using both Markdown and HTML styles.
            You can combine both syntaxes together.

        entities (List of :obj:`~pyrogram.types.MessageEntity`):
            List of special entities that appear in message text, which can be specified instead of *parse_mode*.

        link_preview_options (:obj:`~pyrogram.types.LinkPreviewOptions`, *optional*):
            Link preview generation options for the message.

    """

    def __init__(
        self,
        message_text: str,
        parse_mode: enums.ParseMode | None = None,
        entities: list[types.MessageEntity] | None = None,
        link_preview_options: types.LinkPreviewOptions = None,
        disable_web_page_preview: bool | None = None,
    ) -> None:
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

        super().__init__()

        self.message_text = message_text
        self.parse_mode = parse_mode
        self.entities = entities
        self.link_preview_options = link_preview_options
        # pyroblack <= 2.7.2 name
        self.disable_web_page_preview = (
            disable_web_page_preview
            if disable_web_page_preview is not None
            else (
                getattr(link_preview_options, "is_disabled", None)
                if link_preview_options is not None
                else None
            )
        )

    async def write(self, client: pyrogram.Client, reply_markup):
        message, entities = (
            await utils.parse_text_entities(
                client,
                self.message_text,
                # TODO
                self.parse_mode,
                self.entities,
            )
        ).values()

        if self.link_preview_options is None:
            self.link_preview_options = client.link_preview_options

        if self.link_preview_options and self.link_preview_options.url:
            return raw.types.InputBotInlineMessageMediaWebPage(
                invert_media=self.link_preview_options.show_above_text,
                force_large_media=self.link_preview_options.prefer_large_media,
                force_small_media=self.link_preview_options.prefer_small_media,
                optional=self.link_preview_options.manual,
                url=self.link_preview_options.url,
                reply_markup=await reply_markup.write(client) if reply_markup else None,
                message=message,
                entities=entities,
            )

        return raw.types.InputBotInlineMessageText(
            no_webpage=self.link_preview_options.is_disabled
            if self.link_preview_options
            else None,
            invert_media=self.link_preview_options.show_above_text
            if self.link_preview_options
            else None,
            reply_markup=await reply_markup.write(client) if reply_markup else None,
            message=message,
            entities=entities,
        )
