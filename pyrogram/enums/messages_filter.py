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


class MessagesFilter(AutoName):
    """Messages filter enumeration used in :meth:`~pyrogram.Client.search_messages` and :meth:`~pyrogram.Client.search_global`"""

    EMPTY = raw.functions.InputMessagesFilterEmpty
    "Empty filter (any kind of messages)"

    PHOTO = raw.functions.InputMessagesFilterPhotos
    "Photo messages"

    VIDEO = raw.functions.InputMessagesFilterVideo
    "Video messages"

    PHOTO_VIDEO = raw.functions.InputMessagesFilterPhotoVideo
    "Photo and video messages"

    DOCUMENT = raw.functions.InputMessagesFilterDocument
    "Document messages"

    URL = raw.functions.InputMessagesFilterUrl
    "Messages containing URLs"

    ANIMATION = raw.functions.InputMessagesFilterGif
    "Animation messages"

    VOICE_NOTE = raw.functions.InputMessagesFilterVoice
    "Voice note messages"

    VIDEO_NOTE = raw.functions.InputMessagesFilterRoundVideo
    "Video note messages"

    AUDIO_VIDEO_NOTE = raw.functions.InputMessagesFilterRoundVideo
    "Audio and video note messages"

    AUDIO = raw.functions.InputMessagesFilterMusic
    "Audio messages (music)"

    CHAT_PHOTO = raw.functions.InputMessagesFilterChatPhotos
    "Chat photo messages"

    PHONE_CALL = raw.functions.InputMessagesFilterPhoneCalls
    "Phone call messages"

    MENTION = raw.functions.InputMessagesFilterMyMentions
    "Messages containing mentions"

    LOCATION = raw.functions.InputMessagesFilterGeo
    "Location messages"

    CONTACT = raw.functions.InputMessagesFilterContacts
    "Contact messages"

    PINNED = raw.functions.InputMessagesFilterPinned
    "Pinned messages"
