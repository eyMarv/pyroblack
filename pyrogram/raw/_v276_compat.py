#  Pyroblack - Telegram MTProto API Client Library for Python
#  Copyright (C) 2024-present eyMarv <https://github.com/eyMarv>
#  Maintainer: irisXDR <https://github.com/irisXDR>
#
#  Low-level raw TL compatibility shims for pyroblack <= 2.7.6.
#
#  During the rebase to Layer 228, Telegram had moved the forum-topic RPC
#  constructors from the ``channels.*`` namespace to ``messages.*`` (and dropped
#  ``channels.editCreator`` entirely in favour of the transfer-ownership flow on
#  ``channels.editAdmin``). The high-level ``Client`` methods were updated to
#  call the new ``messages.*`` constructors, but any downstream code that
#  imported the raw classes directly — e.g.
#  ``from pyrogram.raw.functions.channels import CreateForumTopic`` — broke with
#  ``ImportError`` because those modules no longer exist in the checked-in raw
#  tree.
#
#  This module restores the seven ``channels.*`` forum constructors as thin
#  subclasses of their ``messages.*`` equivalents. They accept the legacy
#  ``channel`` kwarg (an ``InputChannel``), map it to ``peer`` (an
#  ``InputPeer`` — ``InputChannel`` is a valid ``InputPeer`` on the wire), and
#  preserve the v2.7.6 ``QUALNAME``/``ID`` so ``obj._ == "channels.CreateForumTopic"``
#  comparisons and ``raw.objects[<old_hash>]`` lookups keep working.
#
#  The two *update* types (``updateChannelPinnedTopic`` /
#  ``updateChannelPinnedTopics``) are NOT shimmed: Telegram changed their wire
#  format from ``channel_id:long`` to ``peer:Peer``, so a faithful alias is
#  impossible. See COMPAT_ASSESSMENT.md (L-section) for details.

from __future__ import annotations

from typing import Any

from pyrogram.raw import types as raw_types
from pyrogram.raw.functions import channels as raw_channels
from pyrogram.raw.functions import messages as raw_messages


def _make_channel_alias(messages_cls, legacy_qualname: str, legacy_id: int):
    """Build a ``channels.*`` alias subclass of a ``messages.*`` constructor.

    The legacy constructors took ``channel: InputChannel`` where the new ones
    take ``peer: InputPeer``. We accept ``channel`` (and fall back to ``peer``
    for callers already migrated) and forward every other kwarg unchanged.
    """

    class _ChannelAlias(messages_cls):  # type: ignore[misc, valid-type]
        __slots__ = ()  # inherited from messages_cls

        # Preserve the v2.7.6 identity for ``obj.QUALNAME`` / JSON ``_`` string
        # comparisons. The wire ``ID`` is intentionally NOT overridden: it stays
        # the new ``messages.*`` constructor ID so the server accepts the
        # request (the old ``channels.*`` IDs are dead on Layer 228). The legacy
        # hash is still resolvable via ``raw.objects[<legacy_id>]`` (registered
        # separately in ``install_raw_compat``).
        QUALNAME = legacy_qualname

        def __init__(self, *, channel: Any = None, peer: Any = None, **kwargs: Any) -> None:
            if channel is not None and peer is None:
                peer = channel
            if peer is None:
                # Match the generated classes' behaviour for a missing required arg.
                raise TypeError(
                    f"{legacy_qualname} requires 'channel' (InputChannel)"
                )
            super().__init__(peer=peer, **kwargs)

    # Inherit ``read``/``write`` from the messages.* class unchanged: the wire
    # format is identical (an InputPeer field), and ``write`` emits the new
    # messages.* constructor ID which is the only one the server accepts on
    # Layer 228.

    _ChannelAlias.__name__ = messages_cls.__name__
    _ChannelAlias.__qualname__ = legacy_qualname.rsplit(".", 1)[-1]
    return _ChannelAlias


# (messages class, legacy QUALNAME, legacy constructor ID)
_FORUM_ALIASES = [
    (raw_messages.CreateForumTopic, "functions.channels.CreateForumTopic", 0xF40C0224),
    (raw_messages.EditForumTopic, "functions.channels.EditForumTopic", 0xF4DFA185),
    (raw_messages.GetForumTopics, "functions.channels.GetForumTopics", 0xDE560D1),
    (raw_messages.GetForumTopicsByID, "functions.channels.GetForumTopicsByID", 0xB0831EB9),
    (raw_messages.ReorderPinnedForumTopics, "functions.channels.ReorderPinnedForumTopics", 0x2950A18F),
    (raw_messages.UpdatePinnedForumTopic, "functions.channels.UpdatePinnedForumTopic", 0x6C2D9026),
    (raw_messages.DeleteTopicHistory, "functions.channels.DeleteTopicHistory", 0x34435F2D),
]


def install_raw_compat() -> None:
    """Register the ``channels.*`` forum aliases into the raw namespaces.

    Idempotent: safe to call multiple times (skips already-registered names).
    """
    from pyrogram import raw

    for messages_cls, qualname, legacy_id in _FORUM_ALIASES:
        alias = _make_channel_alias(messages_cls, qualname, legacy_id)
        short_name = messages_cls.__name__
        if not hasattr(raw_channels, short_name):
            setattr(raw_channels, short_name, alias)
        # Register under the legacy constructor hash so raw.objects[<old_id>]
        # resolves to the alias (v2.7.6 keyed objects by hash).
        raw.objects.setdefault(legacy_id, f"pyrogram.raw.functions.channels.{short_name}")


install_raw_compat()
