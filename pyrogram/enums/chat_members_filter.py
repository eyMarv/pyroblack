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


class ChatMembersFilter(AutoName):
    """Chat members filter enumeration used in :meth:`~pyrogram.Client.get_chat_members`"""

    SEARCH = raw.functions.ChannelParticipantsSearch
    "Search for members"

    BANNED = raw.functions.ChannelParticipantsKicked
    "Banned members"

    RESTRICTED = raw.functions.ChannelParticipantsBanned
    "Restricted members"

    BOTS = raw.functions.ChannelParticipantsBots
    "Bots"

    RECENT = raw.functions.ChannelParticipantsRecent
    "Recently active members"

    ADMINISTRATORS = raw.functions.ChannelParticipantsAdmins
    "Administrators"
