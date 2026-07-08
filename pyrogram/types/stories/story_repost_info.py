from pyrogram import raw, types, utils

from ..object import Object


class StoryRepostInfo(Object):
    def __init__(self, *, origin: "types.StoryOrigin" = None, is_content_modified: bool = None):
        super().__init__()
        self.origin = origin
        self.is_content_modified = is_content_modified

    @staticmethod
    def _parse(client, fwd_from: "raw.base.StoryFwdHeader", users: dict, chats: dict):
        from_user = fwd_from.from_id
        origin = None
        if from_user:
            peer_id = utils.get_raw_peer_id(from_user)
            if isinstance(from_user, raw.types.PeerUser):
                fwd_from_chat = types.Chat._parse_user_chat(client, users.get(peer_id, None))
            elif isinstance(from_user, raw.types.PeerChat):
                fwd_from_chat = types.Chat._parse_chat_chat(client, chats.get(peer_id, None))
            else:
                fwd_from_chat = types.Chat._parse_channel_chat(client, chats.get(peer_id, None))
            origin = types.StoryOriginPublicStory(chat=fwd_from_chat, story_id=fwd_from.story_id)
        else:
            origin = types.StoryOriginHiddenUser(poster_name=fwd_from.from_name)
        return StoryRepostInfo(origin=origin, is_content_modified=fwd_from.modified)
