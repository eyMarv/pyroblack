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


class ChatAction(AutoName):
    """Chat action enumeration used in :obj:`~pyrogram.types.ChatEvent`."""

    TYPING = raw.functions.SendMessageTypingAction
    "Typing text message"

    UPLOAD_PHOTO = raw.functions.SendMessageUploadPhotoAction
    "Uploading photo"

    RECORD_VIDEO = raw.functions.SendMessageRecordVideoAction
    "Recording video"

    UPLOAD_VIDEO = raw.functions.SendMessageUploadVideoAction
    "Uploading video"

    RECORD_AUDIO = raw.functions.SendMessageRecordAudioAction
    "Recording audio"

    UPLOAD_AUDIO = raw.functions.SendMessageUploadAudioAction
    "Uploading audio"

    UPLOAD_DOCUMENT = raw.functions.SendMessageUploadDocumentAction
    "Uploading document"

    FIND_LOCATION = raw.functions.SendMessageGeoLocationAction
    "Finding location"

    RECORD_VIDEO_NOTE = raw.functions.SendMessageRecordRoundAction
    "Recording video note"

    UPLOAD_VIDEO_NOTE = raw.functions.SendMessageUploadRoundAction
    "Uploading video note"

    PLAYING = raw.functions.SendMessageGamePlayAction
    "Playing game"

    CHOOSE_CONTACT = raw.functions.SendMessageChooseContactAction
    "Choosing contact"

    SPEAKING = raw.functions.SpeakingInGroupCallAction
    "Speaking in group call"

    IMPORT_HISTORY = raw.functions.SendMessageHistoryImportAction
    "Importing history"

    CHOOSE_STICKER = raw.functions.SendMessageChooseStickerAction
    "Choosing sticker"

    CANCEL = raw.functions.SendMessageCancelAction
    "Cancel ongoing chat action"
