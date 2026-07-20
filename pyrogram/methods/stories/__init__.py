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

from .can_post_stories import CanPostStories
from .can_post_story import CanPostStory
from .copy_story import CopyStory
from .delete_stories import DeleteStories
from .edit_story import EditStory
from .edit_story_caption import EditStoryCaption
from .edit_story_media import EditStoryMedia
from .edit_story_privacy import EditStoryPrivacy
from .enable_stealth_mode import EnableStealthMode
from .forward_story import ForwardStory
from .get_all_stories import GetAllStories
from .get_archived_stories import GetArchivedStories
from .get_chat_active_stories import GetChatActiveStories
from .get_chat_archived_stories import GetChatArchivedStories
from .get_chat_stories import GetChatStories
from .get_pinned_stories import GetPinnedStories
from .get_stories import GetStories
from .get_story_views import GetStoryViews
from .hide_chat_stories import HideChatStories
from .hide_my_story_view import HideMyStoryView
from .pin_chat_stories import PinChatStories
from .post_story import PostStory
from .read_chat_stories import ReadChatStories
from .send_story import SendStory
from .show_chat_stories import ShowChatStories
from .toggle_story_is_posted_to_chat_page import ToggleStoryIsPostedToChatPage
from .unpin_chat_stories import UnpinChatStories
from .view_stories import ViewStories


class Stories(
    CanPostStory,
    DeleteStories,
    EditStory,
    ForwardStory,
    GetChatActiveStories,
    GetChatArchivedStories,
    GetStories,
    HideMyStoryView,
    PostStory,
    ToggleStoryIsPostedToChatPage,
    CanPostStories,
    CopyStory,
    EditStoryCaption,
    EditStoryMedia,
    EditStoryPrivacy,
    EnableStealthMode,
    GetAllStories,
    GetArchivedStories,
    GetChatStories,
    GetPinnedStories,
    GetStoryViews,
    HideChatStories,
    PinChatStories,
    ReadChatStories,
    SendStory,
    ShowChatStories,
    UnpinChatStories,
    ViewStories,
):
    pass
