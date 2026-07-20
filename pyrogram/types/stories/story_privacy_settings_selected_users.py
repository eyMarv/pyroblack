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
from pyrogram import raw

from .story_privacy_settings import StoryPrivacySettings


class StoryPrivacySettingsSelectedUsers(StoryPrivacySettings):
    """The story can be viewed by certain specified users.

    Parameters
    ----------
        user_ids (List of ``int`` | ``str``, *optional*):
            Identifiers of the users; always unknown and empty for non-owned stories.

    """

    def __init__(self, *, user_ids: list[int | str] | None = None) -> None:
        super().__init__()

        self.user_ids = user_ids

    async def write(self, client: pyrogram.Client):
        privacy_rules = []
        _allowed_users = []
        _allowed_chats = []

        if self.user_ids:
            for user in self.user_ids or []:
                peer = await client.resolve_peer(user)
                if isinstance(peer, raw.types.InputPeerUser):
                    _allowed_users.append(peer)
                elif isinstance(peer, raw.types.InputPeerChat):
                    _allowed_chats.append(peer.chat_id)
                elif isinstance(peer, raw.types.InputPeerChannel):
                    _allowed_chats.append(peer.channel_id)
        else:
            privacy_rules.append(
                raw.types.InputPrivacyValueAllowUsers(
                    users=[raw.types.InputPeerEmpty()]
                )
            )

        if _allowed_users:
            privacy_rules.append(
                raw.types.InputPrivacyValueAllowUsers(users=_allowed_users)
            )
        if _allowed_chats:
            privacy_rules.append(
                raw.types.InputPrivacyValueAllowChatParticipants(chats=_allowed_chats)
            )
        return privacy_rules
