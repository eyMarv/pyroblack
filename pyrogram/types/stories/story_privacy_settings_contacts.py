from typing import Union

import pyrogram
from pyrogram import raw

from .story_privacy_settings import StoryPrivacySettings


class StoryPrivacySettingsContacts(StoryPrivacySettings):
    def __init__(self, *, except_user_ids: list[Union[int, str]] = None):
        super().__init__()
        self.except_user_ids = except_user_ids

    async def write(self, client: "pyrogram.Client"):
        privacy_rules = [raw.types.InputPrivacyValueAllowContacts()]
        users = [await client.resolve_peer(user_id) for user_id in (self.except_user_ids or [])]
        if users:
            privacy_rules.append(raw.types.InputPrivacyValueDisallowUsers(users=users))
        return privacy_rules
