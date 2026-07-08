import pyrogram
from pyrogram import raw, types, utils

from ..object import Object


class StoryPrivacySettings(Object):
    def __init__(self):
        super().__init__()

    @staticmethod
    def _parse(client: "pyrogram.Client", privacy_rules: list["raw.base.PrivacyRule"]):
        ko = []
        for priv in privacy_rules:
            if isinstance(priv, raw.types.PrivacyValueAllowAll):
                ko.append(types.StoryPrivacySettingsEveryone())
            if isinstance(priv, raw.types.PrivacyValueDisallowUsers):
                if types.StoryPrivacySettingsEveryone in ko:
                    ko.append(types.StoryPrivacySettingsEveryone(except_user_ids=priv.users))
                if types.StoryPrivacySettingsContacts in ko:
                    ko.append(types.StoryPrivacySettingsContacts(except_user_ids=priv.users))
            if isinstance(priv, raw.types.PrivacyValueAllowContacts):
                ko.append(types.StoryPrivacySettingsContacts())
            if isinstance(priv, raw.types.PrivacyValueAllowCloseFriends):
                ko.append(types.StoryPrivacySettingsCloseFriends())
            if isinstance(priv, raw.types.PrivacyValueAllowUsers):
                ko.append(types.StoryPrivacySettingsSelectedUsers(user_ids=priv.users))
            if isinstance(priv, raw.types.PrivacyValueAllowChatParticipants):
                ko.append(types.StoryPrivacySettingsSelectedUsers(user_ids=[utils.get_channel_id(chat_id) for chat_id in priv.chats]))
        return ko[-1] if len(ko) > 0 else None
