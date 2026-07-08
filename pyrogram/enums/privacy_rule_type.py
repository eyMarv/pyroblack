#  Pyrogram - Telegram MTProto API Client Library for Python
#  Copyright (C) 2017-present Dan <https://github.com/delivrance>
#
#  This file is part of Pyrogram.
#
#  Pyrogram is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Lesser General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
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


class PrivacyRuleType(AutoName):
    """Privacy rule type enumeration used in :obj:`~pyrogram.types.PrivacyRule`."""

    ALLOW_ALL = raw.types.PrivacyValueAllowAll
    "Allow all"

    ALLOW_BOTS = raw.types.PrivacyValueAllowBots
    "Allow only bots"

    ALLOW_CHAT_PARTICIPANTS = raw.types.PrivacyValueAllowChatParticipants
    "Allow only participants of certain chats"

    ALLOW_CLOSE_FRIENDS = raw.types.PrivacyValueAllowCloseFriends
    "Allow only close friends"

    ALLOW_CONTACTS = raw.types.PrivacyValueAllowContacts
    "Allow all contacts"

    ALLOW_PREMIUM = raw.types.PrivacyValueAllowPremium
    "Allow only users with a Premium subscription. Currently only usable for :obj:`~pyrogram.enums.PrivacyKey.CHAT_INVITE`."

    ALLOW_USERS = raw.types.PrivacyValueAllowUsers
    "Allow only certain users"

    DISALLOW_ALL = raw.types.PrivacyValueDisallowAll
    "Disallow all"

    DISALLOW_BOTS = raw.types.PrivacyValueDisallowBots
    "Disallow bots and miniapps"

    DISALLOW_CHAT_PARTICIPANTS = raw.types.PrivacyValueDisallowChatParticipants
    "Disallow only participants of certain chats"

    DISALLOW_CONTACTS = raw.types.PrivacyValueDisallowContacts
    "Disallow contacts only"

    DISALLOW_USERS = raw.types.PrivacyValueDisallowUsers
    "Disallow only certain users"
