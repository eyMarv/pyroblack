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

from .chosen_inline_result import ChosenInlineResult
from .inline_query import InlineQuery
from .inline_query_result import InlineQueryResult
from .inline_query_result_animation import InlineQueryResultAnimation
from .inline_query_result_article import InlineQueryResultArticle
from .inline_query_result_audio import InlineQueryResultAudio
from .inline_query_result_cached_animation import InlineQueryResultCachedAnimation
from .inline_query_result_cached_audio import InlineQueryResultCachedAudio
from .inline_query_result_cached_document import InlineQueryResultCachedDocument
from .inline_query_result_cached_photo import InlineQueryResultCachedPhoto
from .inline_query_result_cached_sticker import InlineQueryResultCachedSticker
from .inline_query_result_cached_video import InlineQueryResultCachedVideo
from .inline_query_result_cached_voice import InlineQueryResultCachedVoice
from .inline_query_result_contact import InlineQueryResultContact
from .inline_query_result_document import InlineQueryResultDocument
from .inline_query_result_game import InlineQueryResultGame
from .inline_query_result_location import InlineQueryResultLocation
from .inline_query_result_photo import InlineQueryResultPhoto
from .inline_query_result_venue import InlineQueryResultVenue
from .inline_query_result_video import InlineQueryResultVideo
from .inline_query_result_voice import InlineQueryResultVoice

__all__ = [
    "ChosenInlineResult",
    "InlineQuery",
    "InlineQueryResult",
    "InlineQueryResultAnimation",
    "InlineQueryResultArticle",
    "InlineQueryResultAudio",
    "InlineQueryResultCachedAnimation",
    "InlineQueryResultCachedAudio",
    "InlineQueryResultCachedDocument",
    "InlineQueryResultCachedPhoto",
    "InlineQueryResultCachedSticker",
    "InlineQueryResultCachedVideo",
    "InlineQueryResultCachedVoice",
    "InlineQueryResultContact",
    "InlineQueryResultDocument",
    "InlineQueryResultGame",
    "InlineQueryResultLocation",
    "InlineQueryResultPhoto",
    "InlineQueryResultVenue",
    "InlineQueryResultVideo",
    "InlineQueryResultVoice",
]
