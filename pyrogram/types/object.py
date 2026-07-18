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

import re
from datetime import datetime
from enum import Enum
from json import dumps

import pyrogram


class Object:
    # Soft aliases for pyroblack <= 2.7.2 attribute names that were renamed
    # after the 2.8+ rebase. Only used when the attr is missing on the instance.
    # Prefer dual-setting on Message/Chat.__init__ when shapes differ (int vs object).
    _COMPAT_ALIASES = {
        # User / Chat common
        "raw": "_raw",
        "usernames": "active_usernames",
        "reply_color": "accent_color",
        "active_users_count": "active_user_count",
        "is_contacts_only": "restricts_new_chats",
        "is_bot_business": "can_connect_to_business",
        "is_members_hidden": "has_hidden_members",
        "is_participants_hidden": "has_hidden_members",
        "is_antispam": "has_aggressive_anti_spam_enabled",
        "is_auto_translation_enabled": "has_automatic_translation",
        "birthday": "birthdate",
        # Chat renames
        "wallpaper": "background",
        "is_paid_reactions_available": "can_enable_paid_reaction",
        # Message renames (same-shape or best-effort)
        "invert_media": "show_caption_above_media",
        "video_chat_members_invited": "video_chat_participants_invited",
        "general_topic_hidden": "general_forum_topic_hidden",
        "general_topic_unhidden": "general_forum_topic_unhidden",
        "giveaway_launched": "giveaway_created",
        "giveaway_result": "giveaway_completed",
        "payment_refunded": "refunded_payment",
        "bot_allowed": "write_access_allowed",
        "web_page_preview": "web_page",
        "user_shared": "users_shared",
        "reply_to_top_message_id": "message_thread_id",
        # Dialog / ChatMember / keyboards
        "ttl_period": "message_auto_delete_time",
        "folder_id": "chat_list",
        "subscription_until_date": "until_date",
        "placeholder": "input_field_placeholder",
        "can_send_docs": "can_send_documents",
        "can_send_roundvideos": "can_send_video_notes",
        "can_send_voices": "can_send_voice_notes",
        "can_send_plain": "can_send_messages",
        "old_forum_topic": "old_topic_info",
        "new_forum_topic": "new_topic_info",
        # Inline / session
        "thumb_url": "thumbnail_url",
        "thumb_width": "thumbnail_width",
        "thumb_height": "thumbnail_height",
        "thumb_mime_type": "thumbnail_mime_type",
        "region": "location",
    }

    # Soft defaults for optional flags/attrs old bots always read
    _COMPAT_DEFAULTS = {
        "is_frozen": False,
        "frozen_icon": None,
        "edit_hide": None,
        "video_processing_pending": None,
        "reply_to_chat_id": None,
        "reply_to_story_id": None,
        "reply_to_story_user_id": None,
        "reply_to_story_chat_id": None,
        "boosts_applied": None,
        "chat_ttl_period": None,
        "join_request_approved": None,
        "chat_joined_by_request": None,
        "requested_chats": None,
        "alternative_videos": None,
        "stories": None,
        "linked_forum": None,
        "subscription_until_date": None,
        "business_info": None,
        "folder_id": None,
        "is_join_request": None,
        "is_join_to_send": None,
    }

    def __init__(self, client: "pyrogram.Client" = None):
        self._client = client

    def __getattr__(self, item: str):
        # Called only when normal attribute lookup fails.
        aliases = Object._COMPAT_ALIASES
        if item in aliases:
            try:
                return object.__getattribute__(self, aliases[item])
            except AttributeError:
                return Object._COMPAT_DEFAULTS.get(item)
        if item in Object._COMPAT_DEFAULTS:
            return Object._COMPAT_DEFAULTS[item]
        raise AttributeError(
            f"{type(self).__name__!r} object has no attribute {item!r}"
        )

    def bind(self, client: "pyrogram.Client"):
        """Bind a Client instance to this and to all nested Pyrogram objects.

        Parameters:
            client (:obj:`~pyrogram.types.Client`):
                The Client instance to bind this object with. Useful to re-enable bound methods after serializing and
                deserializing Pyrogram objects with ``repr`` and ``eval``.
        """
        self._client = client

        for i in self.__dict__:
            o = getattr(self, i)

            if isinstance(o, Object):
                o.bind(client)

    @staticmethod
    def default(obj: "Object"):
        if hasattr(obj, "__custom__"):
            _custom_ = obj.__custom__()
            if _custom_ is not None:
                return _custom_

        if isinstance(obj, bytes):
            return repr(obj)

        if isinstance(obj, re.Match):
            return repr(obj)

        if isinstance(obj, Enum):
            return str(obj)

        if isinstance(obj, datetime):
            return str(obj)

        # TODO: #20
        if not hasattr(obj, "__dict__"):
            return obj.__class__.__name__

        return {
            "_": obj.__class__.__name__,
            **{
                attr: (
                    "*" * 9 if attr == "phone_number" else
                    getattr(obj, attr)
                )
                for attr in filter(lambda x: not x.startswith("_"), obj.__dict__)
                if getattr(obj, attr) is not None
            }
        }

    def __str__(self) -> str:
        return dumps(self, indent=4, default=Object.default, ensure_ascii=False)

    def __repr__(self) -> str:
        return "pyrogram.types.{}({})".format(
            self.__class__.__name__,
            ", ".join(
                f"{attr}={repr(getattr(self, attr))}"
                for attr in filter(lambda x: not x.startswith("_"), self.__dict__)
                if getattr(self, attr) is not None
            )
        )

    def __eq__(self, other: "Object") -> bool:
        for attr in self.__dict__:
            try:
                if attr.startswith("_"):
                    continue

                if getattr(self, attr) != getattr(other, attr):
                    return False
            except AttributeError:
                return False

        return True

    def __setstate__(self, state):
        for attr in state:
            obj = state[attr]

            # Maybe a better alternative would be https://docs.python.org/3/library/inspect.html#inspect.signature
            if isinstance(obj, tuple) and len(obj) == 2 and obj[0] == "dt":
                state[attr] = pyrogram.utils.timestamp_to_datetime(obj[1])

        self.__dict__ = state

    def __getstate__(self):
        state = self.__dict__.copy()
        state.pop("_client", None)

        for attr in state:
            obj = state[attr]

            if isinstance(obj, datetime):
                state[attr] = ("dt", obj.timestamp())

        return state
