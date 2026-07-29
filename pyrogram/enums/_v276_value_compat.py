#  Pyroblack - Telegram MTProto API Client Library for Python
#  Copyright (C) 2024-present eyMarv <https://github.com/eyMarv>
#  Maintainer: irisXDR <https://github.com/irisXDR>
#
#  Enum value-string compatibility shims for pyroblack <= 2.7.6.
#
#  Background
#  ----------
#  pyroblack enums subclass ``AutoName``, whose ``_generate_next_value_`` returns
#  ``self.lower()`` — i.e. each member's value is its own lowercased name. During
#  the Layer 228 rebase several members were *renamed* (e.g.
#  ``GIVEAWAY_LAUNCHED`` → ``GIVEAWAY_CREATED``) and kept as aliases of the new
#  member (``GIVEAWAY_LAUNCHED = GIVEAWAY_CREATED``).
#
#  Member-name access and member comparison keep working (the alias resolves to
#  the same member), but two things broke silently:
#
#    1. Reverse lookup by the OLD value string:
#         ``MessageServiceType("giveaway_launched")``  ->  ValueError
#       (the alias member's value is the NEW string ``"giveaway_created"``).
#    2. ``.value`` / ``str()`` / ``json.dumps`` of an alias member returns the
#       NEW string, not the one v2.7.6 code expected.
#
#  This module restores (1) by registering every old value string into the
#  enum's ``_value2member_map_`` so ``Enum("old_value")`` resolves to the alias
#  member. (2) is NOT restored: an alias member necessarily shares one value
#  with its target, so making ``GIVEAWAY_LAUNCHED.value`` differ from
#  ``GIVEAWAY_CREATED.value`` would break the very member-equality that
#  comparison code relies on. See COMPAT_ASSESSMENT.md (Enum section).
#
#  The mapping below was produced by diffing the resolved ``__members__`` of
#  every shared enum between the v2.7.6 tag and HEAD (see the enum-diff audit).
#  Only members whose value string actually changed are listed.

from __future__ import annotations

from pyrogram.enums import (
    ChatEventAction,
    ChatType,
    MessageMediaType,
    MessageOriginType,
    MessageServiceType,
)

# {Enum: {old_value_string: alias_member_name_in_HEAD}}
_VALUE_ALIASES = {
    ChatType: {
        # v2.7.6 had distinct FORUM/MONOFORUM members; HEAD aliases them to
        # SUPERGROUP/CHANNEL (intentional: a forum is a supergroup feature).
        "forum": "SUPERGROUP",
        "monoforum": "CHANNEL",
    },
    ChatEventAction: {
        "created_forum_topic": "CREATED_FORUM_TOPIC",
        "edited_forum_topic": "EDITED_FORUM_TOPIC",
        "deleted_forum_topic": "DELETED_FORUM_TOPIC",
    },
    MessageMediaType: {
        "web_page_preview": "WEB_PAGE",      # renamed to WEB_PAGE
        "unsupported": "UNSUPPORTED",         # renamed to UNKNOWN (alias kept)
    },
    MessageOriginType: {
        "import": "IMPORT",                   # renamed to IMPORT_INFO (alias kept)
    },
    MessageServiceType: {
        "general_topic_hidden": "GENERAL_TOPIC_HIDDEN",
        "general_topic_unhidden": "GENERAL_TOPIC_UNHIDDEN",
        "video_chat_members_invited": "VIDEO_CHAT_MEMBERS_INVITED",
        "giveaway_launched": "GIVEAWAY_LAUNCHED",
        "giveaway_result": "GIVEAWAY_RESULT",
        "chat_ttl_changed": "CHAT_TTL_CHANGED",
        "boost_apply": "BOOST_APPLY",
        "payment_refunded": "PAYMENT_REFUNDED",
        "bot_allowed": "BOT_ALLOWED",
        "unsupported": "UNSUPPORTED",         # renamed to UNKNOWN (alias kept)
        "channelshared": "CHAT_SHARED",       # ChannelShared -> CHAT_SHARED
        "usershared": "USERS_SHARED",         # UserShared -> USERS_SHARED
    },
}


def install_enum_value_compat() -> None:
    """Register old value strings so ``Enum("old_value")`` resolves.

    Idempotent: skips values already present in ``_value2member_map_``.
    """
    for enum_cls, mapping in _VALUE_ALIASES.items():
        value_map = enum_cls._value2member_map_
        for old_value, member_name in mapping.items():
            if old_value in value_map:
                continue  # already registered (or a real member has this value)
            member = getattr(enum_cls, member_name, None)
            if member is None:
                continue  # alias member not present in this build — skip safely
            value_map[old_value] = member


install_enum_value_compat()
