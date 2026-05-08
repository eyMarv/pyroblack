#  pyroblack - Telegram MTProto API Client Library for Python
#  Copyright (C) 2017-present Dan <https://github.com/delivrance>
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

from __future__ import annotations

from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    from pyrogram.types import MessageEntity


class CustomEmoji:
    """Helper class for embedding custom emoji in Telegram messages.

    Telegram supports displaying animated/custom emoji stickers inline in message text.
    This class provides a simple, parse-mode-agnostic interface to build the appropriate
    markup string or :obj:`~pyrogram.types.MessageEntity` object.

    .. note::
        Custom emoji require either:

        - The **sender** to have an active Telegram Premium subscription (for user accounts), **or**
        - The **bot** to have purchased an additional Fragment username (for bots).

        Free custom emoji (from emoji packs marked as free) can be sent by anyone.

    Parameters:
        emoji_id (``int``):
            The unique document identifier of the custom emoji sticker.
            You can obtain this via :meth:`~pyrogram.Client.get_custom_emoji_stickers`
            or by inspecting existing messages that use the emoji.

        text (``str``):
            The fallback text to display when the custom emoji cannot be rendered
            (e.g. on clients that don't support it). Typically the base emoji character
            the sticker is based on (e.g. ``"🔥"``).

    Example:
        .. code-block:: python

            from pyrogram.types import CustomEmoji

            emoji_id = 5309984423003823023  # document ID of the custom emoji

            # --- HTML parse mode (default) ---
            text = f"Hello {CustomEmoji(emoji_id, '🔥').html} world!"
            await app.send_message(chat_id, text)

            # --- Markdown parse mode ---
            from pyrogram.enums import ParseMode
            text = f"Hello {CustomEmoji(emoji_id, '🔥').markdown} world!"
            await app.send_message(chat_id, text, parse_mode=ParseMode.MARKDOWN)

            # --- Using MessageEntity directly (no parse mode needed) ---
            from pyrogram.enums import ParseMode
            emoji = CustomEmoji(emoji_id, '🔥')
            await app.send_message(
                chat_id,
                "Hello 🔥 world!",         # plain text with the fallback emoji in place
                parse_mode=ParseMode.DISABLED,
                entities=emoji.as_entities("Hello 🔥 world!", offset=6),
            )

        Build multiple emojis at once:

        .. code-block:: python

            from pyrogram.types import CustomEmoji

            fire   = CustomEmoji(5309984423003823023, "🔥")
            heart  = CustomEmoji(5368324170671202286, "❤️")

            text = f"{fire.html} Hot stuff {heart.html}!"
            await app.send_message(chat_id, text)
    """

    def __init__(self, emoji_id: int, text: str) -> None:
        self.emoji_id = int(emoji_id)
        self.text = text

    # ------------------------------------------------------------------
    # Markup helpers
    # ------------------------------------------------------------------

    @property
    def html(self) -> str:
        """Return the HTML markup string for this custom emoji.

        Ready to embed directly in any ``text`` argument when using the
        default (HTML or combined) parse mode.

        Example:
            .. code-block:: python

                emoji = CustomEmoji(5309984423003823023, "🔥")
                await app.send_message(chat_id, f"Fire: {emoji.html}")
        """
        return f'<emoji id="{self.emoji_id}">{self.text}</emoji>'

    @property
    def markdown(self) -> str:
        """Return the Markdown markup string for this custom emoji.

        Ready to embed directly in any ``text`` argument when using
        :obj:`~pyrogram.enums.ParseMode.MARKDOWN`.

        Example:
            .. code-block:: python

                from pyrogram.enums import ParseMode
                emoji = CustomEmoji(5309984423003823023, "🔥")
                await app.send_message(
                    chat_id,
                    f"Fire: {emoji.markdown}",
                    parse_mode=ParseMode.MARKDOWN,
                )
        """
        return f"![{self.text}](tg://emoji?id={self.emoji_id})"

    def as_entities(
        self,
        full_text: str,
        offset: int,
    ) -> List["MessageEntity"]:
        """Build a :obj:`~pyrogram.types.MessageEntity` list for this emoji.

        Use this when ``parse_mode`` is set to
        :obj:`~pyrogram.enums.ParseMode.DISABLED` and you want to pass
        entities directly.  The ``full_text`` must be the final plain text
        of your message (with the fallback ``text`` already placed at
        ``offset``).

        Parameters:
            full_text (``str``):
                The plain text of the complete message.  Used only to
                validate that the fallback text is present at ``offset``.

            offset (``int``):
                Character offset (in UTF-16 code units) where this emoji
                starts inside ``full_text``.

        Returns:
            List[:obj:`~pyrogram.types.MessageEntity`]: A one-element list
            containing the ``CUSTOM_EMOJI`` entity.

        Example:
            .. code-block:: python

                from pyrogram.enums import ParseMode
                from pyrogram.types import CustomEmoji

                emoji  = CustomEmoji(5309984423003823023, "🔥")
                msg    = "Hello 🔥 world!"
                # '🔥' starts at character 6 inside the string
                entities = emoji.as_entities(msg, offset=6)

                await app.send_message(
                    chat_id,
                    msg,
                    parse_mode=ParseMode.DISABLED,
                    entities=entities,
                )
        """
        # Import lazily to avoid circular imports
        from pyrogram.types import MessageEntity
        from pyrogram.enums import MessageEntityType

        return [
            MessageEntity(
                type=MessageEntityType.CUSTOM_EMOJI,
                offset=offset,
                length=len(self.text),
                custom_emoji_id=self.emoji_id,
            )
        ]

    # ------------------------------------------------------------------
    # Dunder helpers
    # ------------------------------------------------------------------

    def __str__(self) -> str:
        """Return the HTML markup (default string representation)."""
        return self.html

    def __repr__(self) -> str:
        return f"CustomEmoji(emoji_id={self.emoji_id!r}, text={self.text!r})"

    # ------------------------------------------------------------------
    # Class-level convenience factory
    # ------------------------------------------------------------------

    @classmethod
    def html_list(cls, emojis: List["CustomEmoji"], separator: str = "") -> str:
        """Join multiple :obj:`CustomEmoji` objects as HTML markup.

        Parameters:
            emojis (List[:obj:`CustomEmoji`]):
                The emoji objects to join.

            separator (``str``, *optional*):
                String to place between each emoji markup.
                Defaults to empty string.

        Returns:
            ``str``: The combined HTML markup string.

        Example:
            .. code-block:: python

                from pyrogram.types import CustomEmoji

                emojis = [
                    CustomEmoji(5309984423003823023, "🔥"),
                    CustomEmoji(5368324170671202286, "❤️"),
                ]
                text = CustomEmoji.html_list(emojis, separator=" ")
                await app.send_message(chat_id, text)
        """
        return separator.join(e.html for e in emojis)
