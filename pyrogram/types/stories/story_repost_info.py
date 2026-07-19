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


from __future__ import annotations

import pyrogram
from pyrogram import raw, types, utils
from pyrogram.types.object import Object


class StoryRepostInfo(Object):
    """Contains information about original story that was reposted.

    Parameters
    ----------
        origin (:obj:`~pyrogram.types.StoryOrigin`):
            Origin of the story that was reposted.

        is_content_modified (``bool``):
            True, if story content was modified during reposting; otherwise, story wasn't modified.

    """

    def __init__(
        self,
        *,
        origin: types.StoryOrigin = None,
        is_content_modified: bool | None = None,
    ) -> None:
        super().__init__()

        self.origin = origin
        self.is_content_modified = is_content_modified

    @staticmethod
    def _parse(
        client: pyrogram.Client,
        fwd_from: raw.base.StoryFwdHeader,
        users: dict,
        chats: dict,
    ) -> StoryRepostInfo:
        from_user = fwd_from.is_from
        origin = None
        if from_user:
            fwd_from_chat = None
            peer_id = utils.get_peer_id(from_user)
            if isinstance(from_user, raw.types.PeerUser):
                fwd_from_chat = types.Chat._parse_user_chat(client, users.get(peer_id))
            elif isinstance(from_user, raw.types.PeerChat):
                fwd_from_chat = types.Chat._parse_chat_chat(client, chats.get(peer_id))
            else:
                fwd_from_chat = types.Chat._parse_channel_chat(
                    client, chats.get(peer_id)
                )
            origin = types.StoryOriginPublicStory(
                chat=fwd_from_chat,
                story_id=fwd_from.story_id,
            )
        else:
            origin = types.StoryOriginHiddenUser(
                poster_name=fwd_from.from_name,
            )
        return StoryRepostInfo(
            origin=origin,
            is_content_modified=fwd_from.modified,
        )
