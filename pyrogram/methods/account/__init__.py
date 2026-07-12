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

from .get_account_ttl import GetAccountTTL
from .get_privacy import GetPrivacy
from .set_account_ttl import SetAccountTTL
from .set_inactive_session_ttl import SetInactiveSessionTTL
from .set_privacy import SetPrivacy
from .add_profile_audio import AddProfileAudio
from .get_global_privacy_settings import GetGlobalPrivacySettings
from .remove_profile_audio import RemoveProfileAudio
from .set_global_privacy_settings import SetGlobalPrivacySettings
from .set_profile_audio_position import SetProfileAudioPosition


class Account(
    GetAccountTTL,
    GetPrivacy,
    SetAccountTTL,
    SetInactiveSessionTTL,
    SetPrivacy,
    AddProfileAudio,
    GetGlobalPrivacySettings,
    RemoveProfileAudio,
    SetGlobalPrivacySettings,
    SetProfileAudioPosition,
):
    pass
