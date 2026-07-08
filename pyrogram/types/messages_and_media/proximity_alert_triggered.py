from typing import Dict

from pyrogram import types, utils

from ..object import Object


class ProximityAlertTriggered(Object):
    """Information about a proximity alert."""

    def __init__(
        self,
        *,
        traveler,
        watcher,
        distance: str
    ):
        super().__init__()

        self.traveler = traveler
        self.watcher = watcher
        self.distance = distance

    @staticmethod
    def _parse(client, action, users: Dict[int, "raw.base.User"], chats: Dict[int, "raw.base.Chat"]):
        from_id = utils.get_raw_peer_id(action.from_id)
        to_id = utils.get_raw_peer_id(action.to_id)

        return ProximityAlertTriggered(
            traveler=types.Chat._parse_chat(client, users.get(from_id) or chats.get(from_id)),
            watcher=types.Chat._parse_chat(client, users.get(to_id) or chats.get(to_id)),
            distance=action.distance,
        )
