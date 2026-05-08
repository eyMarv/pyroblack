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

from pyrogram import raw
from .auto_name import AutoName


class MessageEntityType(AutoName):
    """Message entity type enumeration used in :obj:`~pyrogram.types.MessageEntity`."""

    MENTION = raw.functions.MessageEntityMention
    "``@username``"

    HASHTAG = raw.functions.MessageEntityHashtag
    "``#hashtag``"

    CASHTAG = raw.functions.MessageEntityCashtag
    "``$USD``"

    BOT_COMMAND = raw.functions.MessageEntityBotCommand
    "``/start@pyrogrambot``"

    URL = raw.functions.MessageEntityUrl
    "``https://pyrogram.org`` (see ``url``)"

    EMAIL = raw.functions.MessageEntityEmail
    "``do-not-reply@pyrogram.org``"

    PHONE_NUMBER = raw.functions.MessageEntityPhone
    "``+1-123-456-7890``"

    BOLD = raw.functions.MessageEntityBold
    "Bold text"

    ITALIC = raw.functions.MessageEntityItalic
    "Italic text"

    UNDERLINE = raw.functions.MessageEntityUnderline
    "Underlined text"

    STRIKETHROUGH = raw.functions.MessageEntityStrike
    "Strikethrough text"

    SPOILER = raw.functions.MessageEntitySpoiler
    "Spoiler text"

    CODE = raw.functions.MessageEntityCode
    "Monowidth string"

    PRE = raw.functions.MessageEntityPre
    "Monowidth block (see ``language``)"

    BLOCKQUOTE = raw.functions.MessageEntityBlockquote
    "Blockquote text"

    EXPANDABLE_BLOCKQUOTE = raw.functions.MessageEntityBlockquote
    "collapsed-by-default block quotation"

    TEXT_LINK = raw.functions.MessageEntityTextUrl
    "For clickable text URLs"

    TEXT_MENTION = raw.functions.MessageEntityMentionName
    "for users without usernames (see ``user``)"

    BANK_CARD = raw.functions.MessageEntityBankCard
    "Bank card text"

    CUSTOM_EMOJI = raw.functions.MessageEntityCustomEmoji
    "Custom emoji"

    UNKNOWN = raw.functions.MessageEntityUnknown
    "Unknown message entity type"
