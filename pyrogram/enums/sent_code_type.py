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


class SentCodeType(AutoName):
    """Sent code type enumeration used in :obj:`~pyrogram.types.SentCode`."""

    APP = raw.functions.auth.SentCodeTypeApp
    "The code was sent through the telegram app."

    CALL = raw.functions.auth.SentCodeTypeCall
    "The code will be sent via a phone call. A synthesized voice will tell the user which verification code to input."

    FLASH_CALL = raw.functions.auth.SentCodeTypeFlashCall
    "The code will be sent via a flash phone call, that will be closed immediately."

    MISSED_CALL = raw.functions.auth.SentCodeTypeMissedCall
    "Missed call."

    SMS = raw.functions.auth.SentCodeTypeSms
    "The code was sent via SMS."

    FRAGMENT_SMS = raw.functions.auth.SentCodeTypeFragmentSms
    "The code was sent via Fragment SMS."

    EMAIL_CODE = raw.functions.auth.SentCodeTypeEmailCode
    "The code was sent via email."

    FIREBASE_SMS = raw.functions.auth.SentCodeTypeFirebaseSms
    "The code should be delivered via SMS after Firebase attestation."

    SETUP_EMAIL_REQUIRED = raw.functions.auth.SentCodeTypeSetUpEmailRequired
    "The user should add and verify an email address in order to login."

    SMS_PHRASE = raw.functions.auth.SentCodeTypeSmsPhrase
    "The code was sent via SMS with a phrase."

    SMS_WORD = raw.functions.auth.SentCodeTypeSmsWord
    "The code was sent via SMS with a word."
