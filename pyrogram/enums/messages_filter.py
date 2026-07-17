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

from pyrogram import raw
from .auto_name import AutoName


class MessagesFilter(AutoName):
    """Messages filter enumeration used in :meth:`~pyrogram.Client.search_messages` and :meth:`~pyrogram.Client.search_global`"""

    EMPTY = raw.types.InputMessagesFilterEmpty
    "Empty filter (Filter is absent.)"

    PHOTO = raw.types.InputMessagesFilterPhotos
    "Photo messages"

    VIDEO = raw.types.InputMessagesFilterVideo
    "Video messages"

    PHOTO_VIDEO = raw.types.InputMessagesFilterPhotoVideo
    "Photo and video messages"

    DOCUMENT = raw.types.InputMessagesFilterDocument
    "Document messages"

    URL = raw.types.InputMessagesFilterUrl
    "Messages containing URLs"

    ANIMATION = raw.types.InputMessagesFilterGif
    "Animation messages"

    VOICE_NOTE = raw.types.InputMessagesFilterVoice
    "Voice note messages"

    VIDEO_NOTE = raw.types.InputMessagesFilterRoundVideo
    "Video note messages"

    VOICE_VIDEO_NOTE = raw.types.InputMessagesFilterRoundVoice
    "Voice and video note messages"

    # Alias for pyroblack <= 2.7.2
    AUDIO_VIDEO_NOTE = VOICE_VIDEO_NOTE
    "Deprecated alias of VOICE_VIDEO_NOTE"

    AUDIO = raw.types.InputMessagesFilterMusic
    "Audio messages (music)"

    CHAT_PHOTO = raw.types.InputMessagesFilterChatPhotos
    "Chat photo messages"

    PHONE_CALL = raw.types.InputMessagesFilterPhoneCalls  # TODO
    "Phone call messages"

    MENTION = raw.types.InputMessagesFilterMyMentions
    "Messages containing mentions"

    LOCATION = raw.types.InputMessagesFilterGeo
    "Location messages"

    CONTACT = raw.types.InputMessagesFilterContacts
    "Contact messages"

    PINNED = raw.types.InputMessagesFilterPinned
    "Pinned messages"

    POLL = raw.types.InputMessagesFilterPoll
    "Poll messages"
