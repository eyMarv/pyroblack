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

from typing import List, Optional

import pyrogram
from pyrogram import enums, raw, types, utils
from .inline_session import get_session


class EditInlineText:
    async def edit_inline_text(
        self: "pyrogram.Client",
        inline_message_id: str,
        text: str,
        parse_mode: Optional["enums.ParseMode"] = None,
        entities: Optional[List["types.MessageEntity"]] = None,
        disable_web_page_preview: bool = None,
        link_preview_options: Optional["types.LinkPreviewOptions"] = None,
        reply_markup: "types.InlineKeyboardMarkup" = None,
        invert_media: bool = None,
    ) -> bool:
        """Edit the text of inline messages.

        .. include:: /_includes/usable-by/bots.rst

        Parameters:
            inline_message_id (``str``):
                Identifier of the inline message.

            text (``str``):
                New text of the message.

            parse_mode (:obj:`~pyrogram.enums.ParseMode`, *optional*):
                By default, texts are parsed using both Markdown and HTML styles.
                You can combine both syntaxes together.

            entities (List of :obj:`~pyrogram.types.MessageEntity`, *optional*):
                List of special entities that appear in message text, which can be specified
                instead of *parse_mode*.

            disable_web_page_preview (``bool``, *optional*):
                Disables link previews for links in this message.
                Deprecated: use ``link_preview_options`` instead.

            link_preview_options (:obj:`~pyrogram.types.LinkPreviewOptions`, *optional*):
                Link preview generation options for the message.

            reply_markup (:obj:`~pyrogram.types.InlineKeyboardMarkup`, *optional*):
                An InlineKeyboardMarkup object.

            invert_media (``bool``, *optional*):
                True, If the media position is inverted.
                only animation, photo, video, and webpage preview messages.

        Returns:
            ``bool``: On success, True is returned.

        Example:
            .. code-block:: python

                # Simple edit text
                await app.edit_inline_text(inline_message_id, "new text")

                # Edit text with link preview options
                await app.edit_inline_text(
                    inline_message_id, "check this out",
                    link_preview_options=types.LinkPreviewOptions(is_disabled=True))
        """
        if disable_web_page_preview and link_preview_options is None:
            link_preview_options = types.LinkPreviewOptions(
                is_disabled=disable_web_page_preview
            )

        message, entities = (
            await utils.parse_text_entities(self, text, parse_mode, entities)
        ).values()

        unpacked = utils.unpack_inline_message_id(inline_message_id)
        dc_id = unpacked.dc_id
        session = await get_session(self, dc_id)

        return await session.invoke(
            raw.functions.messages.EditInlineBotMessage(
                id=unpacked,
                no_webpage=link_preview_options.is_disabled if link_preview_options else None,
                reply_markup=await reply_markup.write(self) if reply_markup else None,
                message=message,
                entities=entities,
                invert_media=invert_media,
            ),
            sleep_threshold=self.sleep_threshold,
        )
