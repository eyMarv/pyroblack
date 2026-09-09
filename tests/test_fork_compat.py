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
#  You should have received a copy of the GNU Lesser General Public License
#  along with Pyroblack.  If not, see <http://www.gnu.org/licenses/>.

"""Cross-fork compatibility: decorator aliases and methods ported from
kurigram, wzgram and DzGram.

These do not hit the network. The channel toggles are exercised against a stub
client that records the raw query instead of sending it.
"""

from __future__ import annotations

import asyncio
import inspect

import pytest

from pyrogram import Client, raw


# --------------------------------------------------------------------------- #
# Decorator spellings used by the other forks
# --------------------------------------------------------------------------- #
FORK_DECORATOR_ALIASES = [
    ("on_business_connect", "on_bot_business_connect"),
    ("on_business_connection", "on_bot_business_connection"),
    ("on_business_message", "on_bot_business_message"),
    ("on_deleted_business_messages", "on_deleted_bot_business_messages"),
    ("on_edited_business_message", "on_edited_bot_business_message"),
    ("on_message_reaction", "on_message_reaction_updated"),
    ("on_message_reaction_count", "on_message_reaction_count_updated"),
    ("on_purchased_paid_media", "on_bot_purchased_paid_media"),
]


@pytest.mark.parametrize(("alias", "canonical"), FORK_DECORATOR_ALIASES)
def test_fork_decorator_alias_is_the_same_function(alias: str, canonical: str) -> None:
    aliased = getattr(Client, alias, None)
    assert aliased is not None, f"Client.{alias} is missing"
    assert aliased is getattr(Client, canonical)


def test_fork_decorator_alias_registers_the_same_handler() -> None:
    """Using the alias must build the pyroblack handler, not a second one."""
    from pyrogram.handlers import BotBusinessMessageHandler

    @Client.on_business_message()
    def handler(client, message) -> None:  # pragma: no cover - never called
        pass

    registered = [h for h, _group in handler.handlers]
    assert len(registered) == 1
    assert isinstance(registered[0], BotBusinessMessageHandler)


# --------------------------------------------------------------------------- #
# Channel/supergroup toggles ported from wzgram and kurigram
# --------------------------------------------------------------------------- #
class _RecordingClient(Client):
    """A Client that records the raw queries it would have sent."""

    def __init__(self) -> None:
        from pyrogram.client import Cache

        self.sent: list = []
        self.message_cache = Cache(16)

    fetch_replies = 0

    async def invoke(self, query, *args, **kwargs):
        self.sent.append(query)

        class _Result:
            updates: list = []
            users: list = []
            chats: list = []

        return _Result()

    async def resolve_peer(self, peer_id):
        return raw.types.InputPeerChannel(channel_id=abs(peer_id), access_hash=0)


def _call(factory):
    """Await a Client method from inside a running loop.

    ``pyrogram.sync`` rewrites the async methods on ``Client`` so that calling
    one with no loop running executes it and returns the result directly. Tests
    go through a loop to match how applications actually call these.
    """
    result: list = []

    async def main() -> None:
        result.append(await factory())

    asyncio.run(main())
    return result[0]


PORTED_TOGGLES = [
    ("toggle_anti_spam", {}, raw.functions.channels.ToggleAntiSpam),
    ("toggle_auto_translation", {}, raw.functions.channels.ToggleAutotranslation),
    (
        "toggle_participants_hidden",
        {},
        raw.functions.channels.ToggleParticipantsHidden,
    ),
    ("toggle_pre_history_hidden", {}, raw.functions.channels.TogglePreHistoryHidden),
    ("toggle_signatures", {}, raw.functions.channels.ToggleSignatures),
    (
        "toggle_view_forum_as_messages",
        {},
        raw.functions.channels.ToggleViewForumAsMessages,
    ),
    (
        "restrict_sponsored_messages",
        {},
        raw.functions.channels.RestrictSponsoredMessages,
    ),
]


@pytest.mark.parametrize(("method_name", "extra", "expected_type"), PORTED_TOGGLES)
def test_ported_toggle_invokes_expected_raw_function(
    method_name: str,
    extra: dict,
    expected_type: type,
) -> None:
    client = _RecordingClient()

    result = _call(lambda: getattr(client, method_name)(-100123, **extra))

    assert len(client.sent) == 1
    assert isinstance(client.sent[0], expected_type)
    # No service message in the stub response, so the fallback return applies.
    assert result is True


def test_toggle_anti_spam_forwards_enabled_flag() -> None:
    client = _RecordingClient()

    _call(lambda: client.toggle_anti_spam(-100123, enabled=False))
    assert client.sent[-1].enabled is False

    _call(lambda: client.toggle_anti_spam(-100123))
    assert client.sent[-1].enabled is True


def test_toggle_signatures_forwards_both_flags() -> None:
    client = _RecordingClient()

    _call(
        lambda: client.toggle_signatures(
            -100123, signatures_enabled=True, profiles_enabled=True
        )
    )
    query = client.sent[-1]
    assert query.signatures_enabled is True
    assert query.profiles_enabled is True


def test_restrict_sponsored_messages_forwards_restricted_flag() -> None:
    client = _RecordingClient()

    _call(lambda: client.restrict_sponsored_messages(-100123, restricted=False))
    assert client.sent[-1].restricted is False


def test_ported_toggle_returns_parsed_service_message() -> None:
    """When Telegram sends a service message, it is parsed and returned."""

    class _WithServiceMessage(_RecordingClient):
        async def invoke(self, query, *args, **kwargs):
            self.sent.append(query)

            class _Result:
                updates = [
                    raw.types.UpdateNewChannelMessage(
                        message=raw.types.MessageService(
                            id=5,
                            peer_id=raw.types.PeerChannel(channel_id=123),
                            date=0,
                            action=raw.types.MessageActionChatCreate(
                                title="t", users=[]
                            ),
                        ),
                        pts=1,
                        pts_count=1,
                    )
                ]
                users: list = []
                chats = [
                    raw.types.Channel(
                        id=123,
                        title="Test",
                        photo=raw.types.ChatPhotoEmpty(),
                        date=0,
                        megagroup=True,
                    )
                ]

            return _Result()

    client = _WithServiceMessage()
    result = _call(lambda: client.toggle_anti_spam(-100123))

    assert result is not True
    assert result.id == 5


def test_ported_toggles_are_registered_in_the_docs_catalog() -> None:
    """Every ported method must appear in compiler/docs/compiler.py."""
    import re
    from pathlib import Path

    source = Path("compiler/docs/compiler.py").read_text(encoding="utf-8")
    listed: set[str] = set()
    for block in re.findall(r'="""\s*\n(.*?)"""', source, re.S):
        for line in block.splitlines():
            candidate = line.strip()
            if candidate and re.fullmatch(r"[a-z_][a-z0-9_]*", candidate):
                listed.add(candidate)

    for method_name, _extra, _expected in PORTED_TOGGLES:
        assert method_name in listed, f"{method_name} is not in the docs catalog"


def test_docs_catalog_only_lists_real_client_methods() -> None:
    """Catch a catalog entry that no longer resolves on Client."""
    import re
    from pathlib import Path

    source = Path("compiler/docs/compiler.py").read_text(encoding="utf-8")
    listed: set[str] = set()
    for block in re.findall(r'="""\s*\n(.*?)"""', source, re.S):
        for line in block.splitlines():
            candidate = line.strip()
            if candidate and re.fullmatch(r"[a-z_][a-z0-9_]*", candidate):
                listed.add(candidate)

    unresolved = sorted(name for name in listed if not hasattr(Client, name))
    assert unresolved == []


def test_ported_toggle_signatures_are_keyword_friendly() -> None:
    """The flags must be optional so ``await app.toggle_x(chat_id)`` works."""
    for method_name, _extra, _expected in PORTED_TOGGLES:
        params = inspect.signature(
            inspect.unwrap(getattr(Client, method_name))
        ).parameters
        required = [
            name
            for name, param in params.items()
            if name not in ("self", "args", "kwargs")
            and param.default is inspect.Parameter.empty
        ]
        assert required == ["chat_id"], f"{method_name} requires {required}"
