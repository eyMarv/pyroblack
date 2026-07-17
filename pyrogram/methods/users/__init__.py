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


from .block_user import BlockUser
from .check_username import CheckUsername
from .delete_profile_photos import DeleteProfilePhotos
from .export_story_link import ExportStoryLink
from .get_chat_photos import GetChatPhotos
from .get_chat_photos_count import GetChatPhotosCount
from .get_common_chats import GetCommonChats
from .get_default_emoji_statuses import GetDefaultEmojiStatuses
from .get_me import GetMe
from .get_peer_stories import GetPeerStories
from .get_stories_history import GetUserStoriesHistory
from .get_users import GetUsers
from .set_emoji_status import SetEmojiStatus
from .set_profile_photo import SetProfilePhoto
from .set_username import SetUsername
from .unblock_user import UnblockUser
from .update_birthday import UpdateBirthday
from .update_personal_chat import UpdatePersonalChat
from .update_profile import UpdateProfile
from .set_birthdate import SetBirthdate
from .set_personal_chat import SetPersonalChat
from .set_personal_channel import SetPersonalChannel
from .update_status import UpdateStatus
from .delete_account import DeleteAccount


class Users(
    BlockUser,
    CheckUsername,
    DeleteProfilePhotos,
    ExportStoryLink,
    GetChatPhotos,
    GetChatPhotosCount,
    GetCommonChats,
    GetDefaultEmojiStatuses,
    GetMe,
    GetPeerStories,
    GetUserStoriesHistory,
    GetUsers,
    SetEmojiStatus,
    SetProfilePhoto,
    SetUsername,
    UnblockUser,
    UpdateBirthday,
    UpdatePersonalChat,
    UpdateProfile,
    SetBirthdate,
    SetPersonalChat,
    SetPersonalChannel,
    UpdateStatus,
    DeleteAccount
):
    pass
