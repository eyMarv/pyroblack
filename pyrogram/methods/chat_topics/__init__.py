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

from .get_forum_topic_icon_stickers import GetForumTopicIconStickers
from .create_forum_topic import CreateForumTopic
from .edit_forum_topic import EditForumTopic
from .close_forum_topic import CloseForumTopic
from .reopen_forum_topic import ReopenForumTopic
from .hide_forum_topic import HideForumTopic
from .unhide_forum_topic import UnhideForumTopic
from .delete_forum_topic import DeleteForumTopic
from .get_forum_topics import GetForumTopics
from .get_forum_topic import GetForumTopic
from .toggle_forum_topic_is_pinned import ToggleForumTopicIsPinned


class ChatTopics(
    CloseForumTopic,
    CreateForumTopic,
    DeleteForumTopic,
    EditForumTopic,
    GetForumTopic,
    GetForumTopicIconStickers,
    GetForumTopics,
    HideForumTopic,
    ReopenForumTopic,
    UnhideForumTopic,
    ToggleForumTopicIsPinned,
):
    pass
