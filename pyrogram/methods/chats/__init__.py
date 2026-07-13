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


from .add_chat_members import AddChatMembers
from .archive_chats import ArchiveChats
from .ban_chat_member import BanChatMember
from .create_channel import CreateChannel
from .create_group import CreateGroup
from .create_supergroup import CreateSupergroup
from .delete_channel import DeleteChannel
from .delete_chat_photo import DeleteChatPhoto
from .delete_supergroup import DeleteSupergroup
from .delete_user_history import DeleteUserHistory
from .get_chat import GetChat
from .get_chat_event_log import GetChatEventLog
from .get_chat_member import GetChatMember
from .get_chat_members import GetChatMembers
from .get_chat_members_count import GetChatMembersCount
from .get_chat_online_count import GetChatOnlineCount
from .get_dialogs import GetDialogs
from .get_direct_messages_topics_by_id import GetDirectMessagesTopicsByID
from .get_direct_messages_topics import GetDirectMessagesTopics
from .get_dialogs_count import GetDialogsCount
from .get_nearby_chats import GetNearbyChats
from .get_send_as_chats import GetSendAsChats
from .join_chat import JoinChat
from .leave_chat import LeaveChat
from .mark_chat_unread import MarkChatUnread
from .pin_chat_message import PinChatMessage
from .promote_chat_member import PromoteChatMember
from .restrict_chat_member import RestrictChatMember
from .search_chats import SearchChats
from .set_administrator_title import SetAdministratorTitle
from .set_chat_description import SetChatDescription
from .set_chat_direct_messages_group import SetChatDirectMessagesGroup
from .set_chat_permissions import SetChatPermissions
from .set_chat_photo import SetChatPhoto
from .set_chat_protected_content import SetChatProtectedContent
from .set_chat_title import SetChatTitle
from .set_chat_message_auto_delete_time import SetChatMessageAutoDeleteTime
from .set_chat_username import SetChatUsername
from .set_send_as_chat import SetSendAsChat
from .set_slow_mode import SetSlowMode
from .unarchive_chats import UnarchiveChats
from .unban_chat_member import UnbanChatMember
from .unpin_all_chat_messages import UnpinAllChatMessages
from .unpin_chat_message import UnpinChatMessage
from .get_created_chats import GetCreatedChats
from .transfer_chat_ownership import TransferChatOwnership
from .add_profile_audio import AddProfileAudio
from .get_chat_audios_count import GetChatAudiosCount
from .get_chat_audios import GetChatAudios
from .remove_profile_audio import RemoveProfileAudio
from .set_profile_audio_position import SetProfileAudioPosition
from .get_similar_channels import GetSimilarChannels
from .get_personal_channels import GetPersonalChannels
from .get_suitable_discussion_chats import GetSuitableDiscussionChats
from .get_top_chats import GetTopChats
from .set_chat_discussion_group import SetChatDiscussionGroup
from .set_main_profile_tab import SetMainProfileTab
from .set_upgraded_gift_colors import SetUpgradedGiftColors
from .update_chat_notifications import UpdateChatNotifications
from .process_chat_has_protected_content_disable_request import ProcessChatHasProtectedContentDisableRequest
from .reorder_folders import ReorderFolders
from .create_folder import CreateFolder
from .create_folder_invite_link import CreateFolderInviteLink
from .delete_folder_invite_link import DeleteFolderInviteLink
from .edit_folder_invite_link import EditFolderInviteLink
from .get_folder_invite_links import GetFolderInviteLinks
from .get_chats_for_folder_invite_link import GetChatsForFolderInviteLink
from .delete_all_message_reactions import DeleteAllMessageReactions
from .delete_message_reaction import DeleteMessageReaction
from .get_chat_settings import GetChatSettings


class Chats(
    AddChatMembers,
    ArchiveChats,
    BanChatMember,
    CreateChannel,
    CreateGroup,
    CreateSupergroup,
    DeleteChannel,
    DeleteChatPhoto,
    DeleteSupergroup,
    DeleteUserHistory,
    GetChat,
    GetChatEventLog,
    GetChatMember,
    GetChatMembers,
    GetChatMembersCount,
    GetChatOnlineCount,
    GetDialogs,
    GetDirectMessagesTopicsByID,
    GetDirectMessagesTopics,
    GetDialogsCount,
    GetNearbyChats,
    GetSendAsChats,
    JoinChat,
    LeaveChat,
    MarkChatUnread,
    PinChatMessage,
    PromoteChatMember,
    RestrictChatMember,
    SearchChats,
    SetAdministratorTitle,
    SetChatDescription,
    SetChatDirectMessagesGroup,
    SetChatPermissions,
    SetChatPhoto,
    SetChatProtectedContent,
    SetChatTitle,
    SetChatMessageAutoDeleteTime,
    SetChatUsername,
    SetSendAsChat,
    SetSlowMode,
    UnarchiveChats,
    UnbanChatMember,
    UnpinAllChatMessages,
    UnpinChatMessage,
    GetCreatedChats,
    TransferChatOwnership,
    AddProfileAudio,
    GetChatAudiosCount,
    GetChatAudios,
    RemoveProfileAudio,
    SetProfileAudioPosition,
    GetSimilarChannels,
    GetPersonalChannels,
    GetSuitableDiscussionChats,
    GetTopChats,
    SetChatDiscussionGroup,
    SetMainProfileTab,
    SetUpgradedGiftColors,
    UpdateChatNotifications,
    ProcessChatHasProtectedContentDisableRequest,
    ReorderFolders,
    CreateFolder,
    CreateFolderInviteLink,
    DeleteFolderInviteLink,
    EditFolderInviteLink,
    GetFolderInviteLinks,
    GetChatsForFolderInviteLink,
    DeleteAllMessageReactions,
    DeleteMessageReaction,
    GetChatSettings
):
    pass
