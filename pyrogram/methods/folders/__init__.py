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

from .check_chat_folder_invite_link import CheckChatFolderInviteLink
from .create_folder_invite_link import CreateFolderInviteLink
from .delete_folder_invite_link import DeleteFolderInviteLink
from .edit_folder_invite_link import EditFolderInviteLink
from .get_chats_for_folder_invite_link import GetChatsForFolderInviteLink
from .get_folder_invite_links import GetFolderInviteLinks
from .reorder_folders import ReorderFolders


class Folders(
    CheckChatFolderInviteLink,
    CreateFolderInviteLink,
    DeleteFolderInviteLink,
    EditFolderInviteLink,
    GetChatsForFolderInviteLink,
    GetFolderInviteLinks,
    ReorderFolders,
):
    pass
