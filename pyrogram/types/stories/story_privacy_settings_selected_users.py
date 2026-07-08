from typing import Union

from pyrogram import raw

from .story_privacy_settings import StoryPrivacySettings


class StoryPrivacySettingsSelectedUsers(StoryPrivacySettings):
    def __init__(self, *, user_ids: list[Union[int, str]] = None):
        super().__init__()
        self.user_ids = user_ids

    async def write(self, client):
        privacy_rules = []
        allowed_users = []
        allowed_chats = []

        if self.user_ids:
            for user in self.user_ids or []:
                peer = await client.resolve_peer(user)
                if isinstance(peer, raw.types.InputPeerUser):
                    allowed_users.append(peer)
                elif isinstance(peer, raw.types.InputPeerChat):
                    allowed_chats.append(peer.chat_id)
                elif isinstance(peer, raw.types.InputPeerChannel):
                    allowed_chats.append(peer.channel_id)
        else:
            privacy_rules.append(raw.types.InputPrivacyValueAllowUsers(users=[raw.types.InputPeerEmpty()]))

        if allowed_users:
            privacy_rules.append(raw.types.InputPrivacyValueAllowUsers(users=allowed_users))
        if allowed_chats:
            privacy_rules.append(raw.types.InputPrivacyValueAllowChatParticipants(chats=allowed_chats))
        return privacy_rules
