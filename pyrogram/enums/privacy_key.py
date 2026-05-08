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


class PrivacyKey(AutoName):
    """Privacy key enumeration used in :meth:`~pyrogram.Client.set_privacy`."""

    ABOUT = raw.functions.InputPrivacyKeyAbout
    "Whether people can see your bio"

    ADDED_BY_PHONE = raw.functions.InputPrivacyKeyAddedByPhone
    "Whether people can add you to their contact list by your phone number"

    BIRTHDAY = raw.functions.InputPrivacyKeyBirthday
    "Whether the user can see our birthday."

    CHAT_INVITE = raw.functions.InputPrivacyKeyChatInvite
    "Whether people will be able to invite you to chats"

    FORWARDS = raw.functions.InputPrivacyKeyForwards
    "Whether messages forwarded from you will be anonymous"

    PHONE_CALL = raw.functions.InputPrivacyKeyPhoneCall
    "Whether you will accept phone calls"

    PHONE_NUMBER = raw.functions.InputPrivacyKeyPhoneNumber
    "Whether people will be able to see your phone number"

    PHONE_P2P = raw.functions.InputPrivacyKeyPhoneP2P
    "Whether to allow P2P communication during VoIP calls"

    PROFILE_PHOTO = raw.functions.InputPrivacyKeyProfilePhoto
    "Whether people will be able to see your profile picture"

    STATUS = raw.functions.InputPrivacyKeyStatusTimestamp
    "Whether people will be able to see our exact last online timestamp."

    VOICE_MESSAGES = raw.functions.InputPrivacyKeyVoiceMessages
    "Whether people can send you voice messages or round videos (Premium users only)."
