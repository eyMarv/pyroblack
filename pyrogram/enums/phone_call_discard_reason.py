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


class PhoneCallDiscardReason(AutoName):
    """Phone call discard reason enumeration used in :obj:`~pyrogram.types.PhoneCallEnded`."""

    MISSED = raw.types.PhoneCallDiscardReasonMissed
    "The call was ended before the conversation started. It was canceled by the caller or missed by the other party"

    DECLINED = raw.types.PhoneCallDiscardReasonBusy
    "The call was ended before the conversation started. It was declined by the other party"

    DISCONNECTED = raw.types.PhoneCallDiscardReasonDisconnect
    "The call was ended before the conversation started. It was declined by the other party"

    HUNG_UP = raw.types.PhoneCallDiscardReasonHangup
    "The call was ended because one of the parties hung up"

    UPGRADE_TO_CONFERENCE_CALL = raw.types.PhoneCallDiscardReasonMigrateConferenceCall
    "The call was ended because it has been upgraded to a conference call"
