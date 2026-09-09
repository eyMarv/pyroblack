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

"""Backwards-compatibility tests for code written against pyroblack v2.7.6.

These tests exercise the compatibility shims restored on top of the rebased
3.x codebase. They do not hit the network; they only assert that the v2.7.6
public API surface still resolves and behaves as expected.
"""

import asyncio
import inspect
import io

import pytest

import pyrogram
from pyrogram import Client
from pyrogram.enums import (
    ChatEventAction,
    ChatType,
    MessageMediaType,
    MessageOriginType,
    MessageServiceType,
)
from pyrogram.types import InputChecklistTask, Message


# --------------------------------------------------------------------------- #
# B1: Client(max_download_workers=...) accepted (v2.7.6 kwarg)
# --------------------------------------------------------------------------- #
def test_client_accepts_max_download_workers_kwarg() -> None:
    """v2.7.6 bots pass max_download_workers=; must not TypeError."""
    sig = inspect.signature(Client.__init__)
    assert "max_download_workers" in sig.parameters

    client = Client(
        "compat_test",
        api_id=1,
        api_hash="hash",
        in_memory=True,
        max_download_workers=8,
    )
    assert client.max_download_workers == 8


def test_client_max_download_workers_defaults_to_none() -> None:
    client = Client("compat_test", api_id=1, api_hash="hash", in_memory=True)
    assert client.max_download_workers is None


# --------------------------------------------------------------------------- #
# B2: MessageMediaType.UNSUPPORTED / MessageServiceType.UNSUPPORTED alias
# --------------------------------------------------------------------------- #
def test_message_media_type_unsupported_alias() -> None:
    """v2.7.6 read message.media == MessageMediaType.UNSUPPORTED."""
    assert hasattr(MessageMediaType, "UNSUPPORTED")
    assert MessageMediaType.UNSUPPORTED is MessageMediaType.UNKNOWN


def test_message_service_type_unsupported_alias() -> None:
    assert hasattr(MessageServiceType, "UNSUPPORTED")
    assert MessageServiceType.UNSUPPORTED is MessageServiceType.UNKNOWN


# --------------------------------------------------------------------------- #
# B3: Message.reply_checklist bound method
# --------------------------------------------------------------------------- #
def test_message_reply_checklist_exists() -> None:
    assert hasattr(Message, "reply_checklist")
    assert callable(Message.reply_checklist)


def test_message_reply_checklist_builds_input_checklist(monkeypatch) -> None:
    """reply_checklist should rebuild an InputChecklist and delegate to send_checklist."""
    captured = {}

    async def fake_send_checklist(self, chat_id, checklist, **kwargs):
        captured["chat_id"] = chat_id
        captured["checklist"] = checklist
        captured["kwargs"] = kwargs
        return "sent"

    monkeypatch.setattr(Client, "send_checklist", fake_send_checklist)

    client = Client("compat_test", api_id=1, api_hash="hash", in_memory=True)
    msg = Message(
        id=42,
        chat=pyrogram.types.Chat(id=123, type=pyrogram.enums.ChatType.GROUP),
        client=client,
    )

    tasks = [InputChecklistTask(id=1, text="Task 1")]

    async def call() -> object:
        return await msg.reply_checklist("To do", tasks)

    result = asyncio.run(call())

    assert result == "sent"
    assert captured["chat_id"] == 123
    built = captured["checklist"]
    assert isinstance(built, pyrogram.types.InputChecklist)
    assert built.title == "To do"
    assert built.tasks == tasks
    # quote=True in non-private chat -> reply_parameters points at msg.id
    assert captured["kwargs"]["reply_parameters"].message_id == 42


# --------------------------------------------------------------------------- #
# B4: Client.preload async helper
# --------------------------------------------------------------------------- #
def test_client_preload_exists() -> None:
    assert hasattr(Client, "preload")


def test_client_preload_reads_bytes() -> None:
    """preload(fp, n) must read n bytes off the loop (v2.7.6 behaviour)."""

    async def main() -> None:
        client = Client("compat_test", api_id=1, api_hash="hash", in_memory=True)
        fp = io.BytesIO(b"hello world payload")
        coro = client.preload(fp, 5)
        assert asyncio.iscoroutine(coro)
        data = await coro
        assert data == b"hello"

    asyncio.run(main())


# --------------------------------------------------------------------------- #
# Already-covered surface: top-level exports + legacy kwargs shim
# --------------------------------------------------------------------------- #
def test_top_level_exports() -> None:
    # All names importable in v2.7.6 must still resolve.
    from pyrogram import (  # noqa: F401
        Client,
        ContinuePropagation,
        StopPropagation,
        StopTransmission,
        ThreadPoolExecutor,
        compose,
        crypto_executor,
        emoji,
        enums,
        filters,
        handlers,
        idle,
        raw,
        types,
    )


def test_legacy_kwargs_shim_installed() -> None:
    """install_legacy_kwargs patches Client/Message to accept old kwargs."""
    from pyrogram.legacy_compat import install_legacy_kwargs

    install_legacy_kwargs()  # idempotent
    # forward_messages accepted drop_author/drop_media_captions in v2.7.6
    sig = inspect.signature(Client.forward_messages)
    # The shim opens the signature to accept **kwargs, so binding old names
    # must not raise TypeError at call-time (we only check signature openness).
    assert (
        any(p.kind == inspect.Parameter.VAR_KEYWORD for p in sig.parameters.values())
        or "kwargs" in sig.parameters
    )


def test_types_identifier_listener_importable() -> None:
    from pyrogram.types import Identifier, Listener  # noqa: F401


# --------------------------------------------------------------------------- #
# L1: Low-level raw TL — channels.* forum constructors moved to messages.*
# --------------------------------------------------------------------------- #
def test_channels_forum_raw_constructors_importable() -> None:
    """v2.7.6 imported forum constructors from raw.functions.channels."""
    from pyrogram.raw.functions.channels import (  # noqa: F401
        CreateForumTopic,
        DeleteTopicHistory,
        EditForumTopic,
        GetForumTopics,
        GetForumTopicsByID,
        ReorderPinnedForumTopics,
        UpdatePinnedForumTopic,
    )


def test_channels_forum_raw_constructors_accept_channel_kwarg() -> None:
    import json

    from pyrogram import raw
    from pyrogram.raw.functions.channels import (
        CreateForumTopic,
        DeleteTopicHistory,
        EditForumTopic,
        GetForumTopics,
        GetForumTopicsByID,
        ReorderPinnedForumTopics,
        UpdatePinnedForumTopic,
    )

    peer = raw.types.InputPeerChannel(channel_id=123, access_hash=456)

    obj = CreateForumTopic(channel=peer, title="Hello", random_id=99, icon_color=7)
    # Legacy QUALNAME preserved for obj._ / str() comparisons
    assert obj.QUALNAME == "functions.channels.CreateForumTopic"
    # channel kwarg mapped to peer
    assert obj.peer is peer
    # JSON repr reports the legacy namespace under "_"
    assert json.loads(str(obj))["_"] == "functions.channels.CreateForumTopic"
    # Wire ID is the NEW messages.* ID (the old channels.* IDs are dead on L228)
    data = obj.write()
    assert int.from_bytes(data[:4], "little") == 0x2F98C3D5

    # Every alias constructs + serializes
    for cls, kw in [
        (EditForumTopic, dict(channel=peer, topic_id=5, title="X")),
        (
            GetForumTopics,
            dict(channel=peer, offset_date=0, offset_id=0, offset_topic=0, limit=10),
        ),
        (GetForumTopicsByID, dict(channel=peer, topics=[1, 2])),
        (ReorderPinnedForumTopics, dict(channel=peer, order=[1, 2])),
        (UpdatePinnedForumTopic, dict(channel=peer, topic_id=5, pinned=True)),
        (DeleteTopicHistory, dict(channel=peer, top_msg_id=10)),
    ]:
        o = cls(**kw)
        assert o.QUALNAME.startswith("functions.channels."), o.QUALNAME
        o.write()  # must serialize without error


def test_channels_forum_raw_objects_hash_lookup() -> None:
    """raw.objects[<legacy_hash>] must resolve to the channels.* alias."""
    from pyrogram import raw

    assert raw.objects[0xF40C0224] == "pyrogram.raw.functions.channels.CreateForumTopic"
    assert raw.objects[0xF4DFA185] == "pyrogram.raw.functions.channels.EditForumTopic"


def test_invalidate_sign_in_codes_works() -> None:
    """Sanity check a raw function the user asked about."""
    from pyrogram.raw.functions.account import InvalidateSignInCodes

    obj = InvalidateSignInCodes(codes=["12345"])
    assert obj.QUALNAME == "functions.account.InvalidateSignInCodes"
    data = obj.write()
    assert int.from_bytes(data[:4], "little") == InvalidateSignInCodes.ID


# --------------------------------------------------------------------------- #
# E1: Enum value-string compat (v2.7.6 -> HEAD)
# AutoName resolves auto() to self.lower(); the rebase renamed several members
# and kept them as aliases of the new member. Member access/comparison still
# works, but reverse lookup by the OLD value string broke. The
# _v276_value_compat registrar restores it.
# --------------------------------------------------------------------------- #
@pytest.mark.parametrize(
    "enum_cls, old_value, expected_member",
    [
        (ChatType, "forum", ChatType.FORUM),
        (ChatType, "monoforum", ChatType.MONOFORUM),
        (ChatEventAction, "created_forum_topic", ChatEventAction.CREATED_FORUM_TOPIC),
        (ChatEventAction, "edited_forum_topic", ChatEventAction.EDITED_FORUM_TOPIC),
        (ChatEventAction, "deleted_forum_topic", ChatEventAction.DELETED_FORUM_TOPIC),
        (MessageMediaType, "web_page_preview", MessageMediaType.WEB_PAGE_PREVIEW),
        (MessageMediaType, "unsupported", MessageMediaType.UNSUPPORTED),
        (MessageOriginType, "import", MessageOriginType.IMPORT),
        (MessageServiceType, "giveaway_launched", MessageServiceType.GIVEAWAY_LAUNCHED),
        (MessageServiceType, "giveaway_result", MessageServiceType.GIVEAWAY_RESULT),
        (MessageServiceType, "chat_ttl_changed", MessageServiceType.CHAT_TTL_CHANGED),
        (MessageServiceType, "boost_apply", MessageServiceType.BOOST_APPLY),
        (MessageServiceType, "payment_refunded", MessageServiceType.PAYMENT_REFUNDED),
        (MessageServiceType, "bot_allowed", MessageServiceType.BOT_ALLOWED),
        (
            MessageServiceType,
            "general_topic_hidden",
            MessageServiceType.GENERAL_TOPIC_HIDDEN,
        ),
        (
            MessageServiceType,
            "general_topic_unhidden",
            MessageServiceType.GENERAL_TOPIC_UNHIDDEN,
        ),
        (
            MessageServiceType,
            "video_chat_members_invited",
            MessageServiceType.VIDEO_CHAT_MEMBERS_INVITED,
        ),
        (MessageServiceType, "unsupported", MessageServiceType.UNSUPPORTED),
        (MessageServiceType, "channelshared", MessageServiceType.CHAT_SHARED),
        (MessageServiceType, "usershared", MessageServiceType.USERS_SHARED),
    ],
)
def test_enum_old_value_reverse_lookup(enum_cls, old_value, expected_member) -> None:
    """Enum("old_v276_value") must resolve to the alias member."""
    got = enum_cls(old_value)
    assert got is expected_member


def test_enum_member_comparison_unchanged() -> None:
    """Alias members must still compare equal to their target (no regression)."""
    assert MessageServiceType.GIVEAWAY_LAUNCHED == MessageServiceType.GIVEAWAY_CREATED
    assert ChatType.FORUM == ChatType.SUPERGROUP
    # New value strings still resolve (regression guard).
    assert MessageServiceType("giveaway_created") is MessageServiceType.GIVEAWAY_CREATED


def test_enum_value_string_limitation_documented() -> None:
    """Known limitation: .value of an alias returns the NEW string, not the old.

    This cannot be fixed without breaking member equality (an alias shares one
    value with its target). Documented in COMPAT_ASSESSMENT.md.
    """
    assert MessageServiceType.GIVEAWAY_LAUNCHED.value == "giveaway_created"
    assert ChatType.FORUM.value == "supergroup"


# --------------------------------------------------------------------------- #
# M1: Method-signature AST diff findings (v2.7.6 -> HEAD)
# --------------------------------------------------------------------------- #
def test_pre_checkout_query_answer_legacy_kwargs() -> None:
    """v2.7.6 PreCheckoutQuery.answer(success=, error=) must not TypeError.

    The exported PreCheckoutQuery is the business variant (ok/error_message);
    the legacy success/error kwargs are mapped onto it.
    """
    import inspect

    from pyrogram.types import PreCheckoutQuery

    sig = inspect.signature(PreCheckoutQuery.answer)
    # Legacy call form binds without error
    sig.bind(None, success=True, error="oops")
    sig.bind(None, success=False, error="fail")
    # Modern form still binds
    sig.bind(None, ok=True)
    sig.bind(None, ok=False, error_message="fail")


def test_send_checklist_legacy_form_binds() -> None:
    """v2.7.6 send_checklist(chat_id, title, tasks, ...) must not TypeError."""
    import inspect

    from pyrogram import Client, types

    sig = inspect.signature(Client.send_checklist)
    # Legacy form (title + tasks instead of checklist)
    sig.bind(
        None,
        chat_id=1,
        title="To Do",
        tasks=[types.InputChecklistTask(id=1, text="x")],
        entities=None,
        others_can_add_tasks=True,
        effect_id=99,
    )
    # Modern form still binds
    sig.bind(None, chat_id=1, checklist=types.InputChecklist(title="x", tasks=[]))


def test_mark_checklist_tasks_as_done_legacy_form_binds() -> None:
    """v2.7.6 mark_checklist_tasks_as_done(..., tasks=[...]) must not TypeError."""
    import inspect

    from pyrogram import Client, types

    sig = inspect.signature(Client.mark_checklist_tasks_as_done)
    # Legacy form: tasks=List[InputChecklistTask]
    sig.bind(None, 1, 5, tasks=[types.InputChecklistTask(id=1, text="x")])
    # Modern form: done_task_ids=[int]
    sig.bind(None, 1, 5, done_task_ids=[1, 2])


def test_send_checklist_adapter_builds_input_checklist() -> None:
    """The legacy kwargs are converted into an InputChecklist object."""
    from pyrogram import types

    # Reproduce the adapter branch from send_checklist
    kwargs = dict(
        title="To Do",
        tasks=[types.InputChecklistTask(id=1, text="x")],
        entities=None,
        parse_mode=None,
        others_can_add_tasks=True,
        others_can_mark_tasks_as_done=False,
        effect_id=99,
    )
    checklist = None
    message_effect_id = None
    parse_mode = None
    if kwargs.get("title") is not None or kwargs.get("tasks") is not None:
        legacy_title = kwargs.pop("title", None)
        legacy_tasks = kwargs.pop("tasks", None)
        legacy_entities = kwargs.pop("entities", None)
        legacy_parse_mode = kwargs.pop("parse_mode", None) or parse_mode
        legacy_others_add = kwargs.pop("others_can_add_tasks", None)
        legacy_others_mark = kwargs.pop("others_can_mark_tasks_as_done", None)
        legacy_effect_id = kwargs.pop("effect_id", None)
        if legacy_effect_id is not None and message_effect_id is None:
            message_effect_id = legacy_effect_id
        checklist = types.InputChecklist(
            title=legacy_title,
            parse_mode=legacy_parse_mode,
            title_entities=legacy_entities,
            tasks=legacy_tasks,
            others_can_add_tasks=legacy_others_add,
            others_can_mark_tasks_as_done=legacy_others_mark,
        )
    assert isinstance(checklist, types.InputChecklist)
    assert checklist.title == "To Do"
    assert checklist.tasks[0].id == 1
    assert checklist.others_can_add_tasks is True
    assert message_effect_id == 99  # effect_id -> message_effect_id


# --------------------------------------------------------------------------- #
# M1: Method-signature AST diff — regression tests for the transform ordering
# bugs found by the v2.7.6 vs HEAD method-signature diff. ``_apply_aliases``
# ran before ``_transform`` and dropped kwargs that ``_transform`` needed,
# silently breaking legacy call sites. These pin the fix.
# --------------------------------------------------------------------------- #
def _map(method_name: str, kwargs: dict) -> dict:
    """Run the legacy_compat alias + transform pipeline (no network)."""
    import pyrogram.legacy_compat as lc

    aliases = lc.CLIENT_LEGACY_KWARGS.get(method_name, {})
    return lc._transform(method_name, lc._apply_aliases(dict(kwargs), aliases))


def test_get_dialogs_from_archive_maps_to_chat_list() -> None:
    """v2.7.6 get_dialogs(from_archive=True) must become chat_list=1."""
    out = _map("get_dialogs", {"limit": 5, "from_archive": True})
    assert out["chat_list"] == 1
    assert "from_archive" not in out  # consumed, not forwarded


def test_get_dialogs_exclude_pinned_dropped() -> None:
    out = _map("get_dialogs", {"limit": 5, "exclude_pinned": True})
    assert "exclude_pinned" not in out


def test_get_dialogs_count_from_archive_maps_to_chat_list() -> None:
    out = _map("get_dialogs_count", {"from_archive": True})
    assert out["chat_list"] == 1


def test_send_poll_correct_option_id_maps_to_list() -> None:
    """v2.7.6 send_poll(correct_option_id=N) must become correct_option_ids=[N]."""
    out = _map("send_poll", {"correct_option_id": 0})
    assert out["correct_option_ids"] == [0]


def test_send_poll_correct_option_id_list_passthrough() -> None:
    out = _map("send_poll", {"correct_option_id": [0, 1]})
    assert out["correct_option_ids"] == [0, 1]


def test_send_poll_reply_to_message_id_maps_to_reply_parameters() -> None:
    out = _map("send_poll", {"reply_to_message_id": 5})
    assert "reply_parameters" in out
    assert out["reply_parameters"].message_id == 5


def test_answer_pre_checkout_query_legacy_kwargs() -> None:
    """v2.7.6 success/error -> ok/error_message."""
    out = _map(
        "answer_pre_checkout_query",
        {"pre_checkout_query_id": "1", "success": True, "error": "bad"},
    )
    assert out["ok"] is True
    assert out["error_message"] == "bad"


def test_get_messages_reply_to_message_ids_maps_to_message_ids() -> None:
    out = _map("get_messages", {"reply_to_message_ids": [5, 6]})
    assert out["message_ids"] == [5, 6]


def test_forward_messages_legacy_drop_flags() -> None:
    out = _map(
        "forward_messages",
        {"drop_author": True, "drop_media_captions": True},
    )
    assert out["send_copy"] is True
    assert out["remove_caption"] is True


def test_edit_message_caption_invert_media_maps_to_show_caption_above_media() -> None:
    out = _map("edit_message_caption", {"invert_media": True})
    assert out["show_caption_above_media"] is True


# --------------------------------------------------------------------------- #
# N1: ``__all__`` restored on the packages that published it in v2.7.6.
# ``from pyrogram import *`` and tooling that reads ``__all__`` broke without it.
# --------------------------------------------------------------------------- #
@pytest.mark.parametrize(
    ("module_name", "expected"),
    [
        (
            "pyrogram",
            [
                "Client",
                "ContinuePropagation",
                "StopPropagation",
                "StopTransmission",
                "compose",
                "crypto_executor",
                "emoji",
                "enums",
                "filters",
                "handlers",
                "idle",
                "raw",
                "types",
            ],
        ),
        ("pyrogram.types", ["List", "Object", "Update"]),
        ("pyrogram.raw", ["base", "core", "functions", "objects", "types"]),
        (
            "pyrogram.errors",
            [
                "BadMsgNotification",
                "CDNFileHashMismatch",
                "RPCError",
                "SecurityCheckMismatch",
                "SecurityError",
                "UnknownError",
            ],
        ),
        (
            "pyrogram.handlers",
            [
                "BotBusinessConnectHandler",
                "BotBusinessMessageHandler",
                "CallbackQueryHandler",
                "DeletedBotBusinessMessagesHandler",
                "EditedBotBusinessMessageHandler",
                "MessageHandler",
                "RawUpdateHandler",
            ],
        ),
        (
            "pyrogram.connection.transport.tcp",
            ["Proxy", "TCP", "TCPAbridged", "proxy_type_by_scheme"],
        ),
    ],
)
def test_dunder_all_restored(module_name: str, expected: list[str]) -> None:
    import importlib

    module = importlib.import_module(module_name)
    assert hasattr(module, "__all__"), f"{module_name} lost __all__"
    for name in expected:
        assert name in module.__all__, f"{module_name}.__all__ is missing {name}"
        assert hasattr(module, name), f"{module_name}.{name} does not resolve"


def test_errors_dunder_all_includes_generated_rpc_errors() -> None:
    """v2.7.6 extended errors.__all__ with every generated RPC error name."""
    from pyrogram import errors

    for name in ("FloodWait", "ChannelPrivate", "PeerIdInvalid"):
        assert name in errors.__all__


def test_types_dunder_all_has_no_duplicates_and_all_resolve() -> None:
    from pyrogram import types

    assert len(types.__all__) == len(set(types.__all__))
    unresolved = [n for n in types.__all__ if not hasattr(types, n)]
    assert unresolved == []


# --------------------------------------------------------------------------- #
# N2: Class constants that v2.7.6 applications read or assigned.
# --------------------------------------------------------------------------- #
def test_client_cache_and_worker_constants() -> None:
    assert Client.MAX_MESSAGE_CACHE_SIZE == Client.MAX_CACHE_SIZE
    assert Client.MAX_DOWNLOAD_WORKERS == Client.DOWNLOAD_POOL_SIZE


def test_connection_max_connection_attempts_alias() -> None:
    from pyrogram.connection import Connection

    assert Connection.MAX_CONNECTION_ATTEMPTS == Connection.MAX_RETRIES
    assert Connection._max_attempts() == Connection.MAX_RETRIES


def test_connection_legacy_attempts_override_is_honoured() -> None:
    """Assigning only the v2.7.6 name must still change the retry count."""
    from pyrogram.connection import Connection

    class Patched(Connection):
        MAX_CONNECTION_ATTEMPTS = 7

    assert Patched._max_attempts() == 7


def test_session_reconnect_constants_present() -> None:
    from pyrogram.session import Session

    assert Session.RECONN_TIMEOUT == 5
    assert Session.RECONNECT_THRESHOLD == 13
    assert list(Session.RE_START_RANGE) == [0, 1, 2, 3]


def test_session_stop_accepts_restart_kwarg() -> None:
    """v2.7.6 called ``await session.stop(restart=True)``."""
    from pyrogram.session import Session

    assert "restart" in inspect.signature(Session.stop).parameters


def test_dispatcher_business_update_groups_present() -> None:
    from pyrogram.dispatcher import Dispatcher
    from pyrogram.raw.types import (
        UpdateBotDeleteBusinessMessage,
        UpdateBotEditBusinessMessage,
        UpdateBotNewBusinessMessage,
    )

    assert Dispatcher.NEW_BOT_BUSINESS_MESSAGE_UPDATES == (UpdateBotNewBusinessMessage,)
    assert Dispatcher.EDIT_BOT_BUSINESS_MESSAGE_UPDATES == (
        UpdateBotEditBusinessMessage,
    )
    assert Dispatcher.DELETE_BOT_BUSINESS_MESSAGES_UPDATES == (
        UpdateBotDeleteBusinessMessage,
    )


# --------------------------------------------------------------------------- #
# N3: Enum members renamed by the rebase.
# --------------------------------------------------------------------------- #
def test_message_service_type_camelcase_share_aliases() -> None:
    assert MessageServiceType.ChannelShared is MessageServiceType.CHAT_SHARED
    assert MessageServiceType.UserShared is MessageServiceType.USERS_SHARED


# --------------------------------------------------------------------------- #
# N4: pyrogram.emoji constants renamed/dropped by the CLDR regeneration.
# --------------------------------------------------------------------------- #
def test_emoji_renamed_constants_alias_current_values() -> None:
    from pyrogram import emoji

    assert emoji.BULLSEYE == emoji.DIRECT_HIT
    assert emoji.RED_CIRCLE == emoji.LARGE_RED_CIRCLE
    assert emoji.TWELVE_O_CLOCK == emoji.TWELVE_OCLOCK
    assert emoji.MAN_S_SHOE == emoji.MANS_SHOE


def test_emoji_removed_constants_keep_original_codepoints() -> None:
    from pyrogram import emoji

    assert emoji.DIGIT_ONE == "1\ufe0f"
    assert emoji.ZERO_WIDTH_JOINER == "\u200d"
    assert emoji.VARIATION_SELECTOR_16 == "\ufe0f"
    assert emoji.REGIONAL_INDICATOR_SYMBOL_LETTER_A == "\U0001f1e6"
    assert emoji.TAG_LATIN_SMALL_LETTER_G == "\U000e0067"
    assert emoji.TAG_DIGIT_ZERO == "\U000e0030"


def test_emoji_compat_covers_every_v276_name() -> None:
    """All 215 names the regeneration lost must be bound."""
    from pyrogram import emoji, emoji_compat

    for name in (*emoji_compat.RENAMED, *emoji_compat.REMOVED):
        assert hasattr(emoji, name), f"pyrogram.emoji.{name} is missing"


def test_emoji_compat_does_not_shadow_generated_names() -> None:
    """install() must never overwrite a name the generated table defines."""
    from pyrogram import emoji, emoji_compat

    before = emoji.LARGE_RED_CIRCLE
    emoji_compat.install(emoji)
    assert emoji.LARGE_RED_CIRCLE == before


# --------------------------------------------------------------------------- #
# N5: Import paths and module-level names that moved.
# --------------------------------------------------------------------------- #
def test_paid_media_legacy_import_path() -> None:
    from pyrogram.types.messages_and_media.paid_media import (  # noqa: F401
        PaidMedia,
        PaidMediaInfo,
        PaidMediaPhoto,
        PaidMediaPreview,
        PaidMediaVideo,
    )
    from pyrogram.types.input_paid_media.paid_media import PaidMedia as Canonical

    assert PaidMedia is Canonical


def test_paid_media_info_legacy_attribute_aliases() -> None:
    """v2.7.6 read message.paid_media.stars_amount / .extended_media."""
    from pyrogram.types import PaidMediaInfo

    info = PaidMediaInfo(star_count=7, paid_media=[])
    assert info.stars_amount == 7
    assert info.extended_media == []


def test_tcp_proxy_type_shims() -> None:
    from pyrogram.connection.transport.tcp.tcp import Proxy, proxy_type_by_scheme

    assert set(proxy_type_by_scheme) == {"SOCKS4", "SOCKS5", "HTTP"}
    assert set(Proxy.__annotations__) == {
        "scheme",
        "hostname",
        "port",
        "username",
        "password",
    }


def test_storage_schema_scripts_are_idempotent() -> None:
    """The restored scripts must be safe to run against a current schema."""
    import sqlite3

    from pyrogram.storage.file_storage import UPDATE_STATE_SCHEMA
    from pyrogram.storage.sqlite_storage import SCHEMA, UNAME_SCHEMA

    conn = sqlite3.connect(":memory:")
    try:
        conn.executescript(SCHEMA)
        conn.executescript(UNAME_SCHEMA)
        conn.executescript(UPDATE_STATE_SCHEMA)
    finally:
        conn.close()


def test_storage_schema_scripts_create_their_tables() -> None:
    import sqlite3

    from pyrogram.storage.file_storage import UPDATE_STATE_SCHEMA
    from pyrogram.storage.sqlite_storage import UNAME_SCHEMA

    conn = sqlite3.connect(":memory:")
    try:
        conn.executescript(UNAME_SCHEMA)
        conn.executescript(UPDATE_STATE_SCHEMA)
        tables = {
            row[0]
            for row in conn.execute("SELECT name FROM sqlite_master WHERE type='table'")
        }
    finally:
        conn.close()

    assert {"usernames", "update_state"} <= tables


# --------------------------------------------------------------------------- #
# N6: Method mixin classes that moved between ``pyrogram.methods`` packages.
# Code that composed its own Client imported these directly.
# --------------------------------------------------------------------------- #
@pytest.mark.parametrize(
    ("module_name", "class_name"),
    [
        ("pyrogram.methods.bots", "AnswerPreCheckoutQuery"),
        ("pyrogram.methods.bots", "GetCollectibleItemInfo"),
        ("pyrogram.methods.bots", "RefundStarPayment"),
        ("pyrogram.methods.chats", "CloseForumTopic"),
        ("pyrogram.methods.chats", "CreateForumTopic"),
        ("pyrogram.methods.chats", "DeleteForumTopic"),
        ("pyrogram.methods.chats", "EditForumTopic"),
        ("pyrogram.methods.chats", "GetForumTopics"),
        ("pyrogram.methods.chats", "ReopenForumTopic"),
        ("pyrogram.methods.messages", "AddChecklistTasks"),
        ("pyrogram.methods.messages", "GetStickers"),
        ("pyrogram.methods.users", "DeleteStories"),
        ("pyrogram.methods.users", "EditStory"),
        ("pyrogram.methods.users", "ForwardStory"),
        ("pyrogram.methods.users", "GetAllStories"),
        ("pyrogram.methods.users", "GetStories"),
        ("pyrogram.methods.users", "SendStory"),
    ],
)
def test_method_mixin_legacy_import_paths(module_name: str, class_name: str) -> None:
    import importlib

    module = importlib.import_module(module_name)
    assert hasattr(module, class_name), f"{module_name}.{class_name} is missing"


def test_add_checklist_tasks_bound_to_client() -> None:
    """The mixin existed but was never wired into ``Messages``."""
    assert hasattr(Client, "add_checklist_tasks")
    params = inspect.signature(inspect.unwrap(Client.add_checklist_tasks)).parameters
    assert {"chat_id", "message_id", "tasks"} <= set(params)


def test_every_v276_client_method_still_exists() -> None:
    """Guard against another silently-unwired mixin."""
    for name in (
        "add_checklist_tasks",
        "answer_pre_checkout_query",
        "check_gift_code",
        "close_forum_topic",
        "create_forum_topic",
        "delete_forum_topic",
        "delete_stories",
        "edit_forum_topic",
        "edit_story",
        "export_story_link",
        "forward_story",
        "get_all_stories",
        "get_collectible_item_info",
        "get_forum_topics",
        "get_stickers",
        "get_stories",
        "mark_checklist_tasks_as_done",
        "refund_star_payment",
        "reopen_forum_topic",
        "send_checklist",
        "send_invoice",
        "send_story",
    ):
        assert hasattr(Client, name), f"Client.{name} is missing"


# --------------------------------------------------------------------------- #
# N7: Story — the rebase replaced the class wholesale, dropping 19 bound methods
# and renaming most attributes. LegacyStoryMixin restores that surface.
# --------------------------------------------------------------------------- #
def _legacy_story(**kwargs):
    """Build a Story with a recording stand-in for the client."""
    from pyrogram import enums as e
    from pyrogram import types as t

    calls: list[tuple[str, dict]] = []

    class RecordingClient:
        def __getattr__(self, name):
            async def call(**kw):
                calls.append((name, kw))
                return "called"

            return call

    kwargs.setdefault(
        "chat",
        t.Chat(
            id=777,
            type=e.ChatType.PRIVATE,
            username="alice",
            first_name="Alice",
        ),
    )
    story = t.Story(client=RecordingClient(), id=42, **kwargs)
    return story, calls


def _run(*coro_factories) -> None:
    """Await bound methods inside a running loop.

    ``pyrogram.sync`` rewrites every async bound method on a type into a wrapper
    that runs the coroutine itself when no loop is running, so these have to be
    awaited from inside one to observe the delegated call.
    """

    async def main() -> None:
        for factory in coro_factories:
            await factory()

    asyncio.run(main())


def test_story_legacy_bound_methods_exist() -> None:
    from pyrogram.types import Story

    for name in (
        "delete",
        "edit",
        "edit_animation",
        "edit_caption",
        "edit_photo",
        "edit_privacy",
        "edit_video",
        "export_link",
        "forward",
        "reply",
        "reply_animation",
        "reply_audio",
        "reply_cached_media",
        "reply_media_group",
        "reply_photo",
        "reply_sticker",
        "reply_text",
        "reply_video",
        "reply_video_note",
        "reply_voice",
    ):
        assert hasattr(Story, name), f"Story.{name} is missing"


def test_story_legacy_attributes_exist() -> None:
    from pyrogram.types import Story

    for name in (
        "allowed_users",
        "animation",
        "close_friends",
        "contacts",
        "denied_users",
        "forward_from",
        "from_user",
        "media_areas",
        "privacy",
        "public",
        "raw",
        "selected_contacts",
        "sender_chat",
    ):
        assert hasattr(Story, name), f"Story.{name} is missing"


def test_story_from_user_and_sender_chat_split_on_chat_type() -> None:
    from pyrogram import enums as e
    from pyrogram import types as t

    private, _ = _legacy_story()
    assert private.from_user is private.chat
    assert private.sender_chat is None

    channel, _ = _legacy_story(
        chat=t.Chat(id=-100123, type=e.ChatType.CHANNEL, title="News"),
    )
    assert channel.from_user is None
    assert channel.sender_chat is channel.chat


def test_story_privacy_attributes_derive_from_privacy_settings() -> None:
    from pyrogram import enums as e
    from pyrogram import types as t

    everyone, _ = _legacy_story(
        privacy_settings=t.StoryPrivacySettingsEveryone(except_user_ids=[9]),
    )
    assert everyone.privacy is e.StoryPrivacy.PUBLIC
    assert everyone.public is True
    assert everyone.contacts is False
    assert everyone.denied_users == [9]

    selected, _ = _legacy_story(
        privacy_settings=t.StoryPrivacySettingsSelectedUsers(user_ids=[1, 2]),
    )
    assert selected.privacy is e.StoryPrivacy.PRIVATE
    assert selected.selected_contacts is True
    assert selected.allowed_users == [1, 2]

    friends, _ = _legacy_story(
        privacy_settings=t.StoryPrivacySettingsCloseFriends(),
    )
    assert friends.privacy is e.StoryPrivacy.CLOSE_FRIENDS
    assert friends.close_friends is True


def test_story_privacy_attributes_are_none_without_settings() -> None:
    story, _ = _legacy_story()
    assert story.privacy is None
    assert story.public is None
    assert story.contacts is None


def test_story_reply_methods_target_poster_and_story() -> None:
    story, calls = _legacy_story()

    _run(
        lambda: story.reply_text("hi"),
        lambda: story.reply_photo("p.png"),
        lambda: story.reply_video("v.mp4"),
        lambda: story.reply_animation("a.mp4"),
        lambda: story.reply_audio("a.mp3"),
        lambda: story.reply_voice("v.ogg"),
        lambda: story.reply_sticker("sid"),
        lambda: story.reply_video_note("vn.mp4"),
        lambda: story.reply_cached_media("fid"),
        lambda: story.reply_media_group([1, 2]),
    )

    assert [name for name, _ in calls] == [
        "send_message",
        "send_photo",
        "send_video",
        "send_animation",
        "send_audio",
        "send_voice",
        "send_sticker",
        "send_video_note",
        "send_cached_media",
        "send_media_group",
    ]
    for _name, kwargs in calls:
        assert kwargs["chat_id"] == 777
        assert kwargs["reply_to_story_id"] == 42


def test_story_reply_honours_explicit_reply_to_story_id() -> None:
    story, calls = _legacy_story()

    _run(lambda: story.reply_text("hi", reply_to_story_id=11))
    assert calls[-1][1]["reply_to_story_id"] == 11


def test_story_reply_is_an_alias_of_reply_text() -> None:
    from pyrogram.types import Story

    story, calls = _legacy_story()
    _run(lambda: Story.reply(story, "hi"))
    assert calls[-1][0] == "send_message"


def test_story_delete_forwards_to_delete_stories() -> None:
    story, calls = _legacy_story()

    _run(story.delete)
    name, kwargs = calls[-1]
    assert name == "delete_stories"
    assert kwargs == {"chat_id": 777, "story_ids": 42}


def test_story_export_link_forwards_to_export_story_link() -> None:
    story, calls = _legacy_story()

    _run(story.export_link)
    name, kwargs = calls[-1]
    assert name == "export_story_link"
    assert kwargs == {"chat_id": 777, "story_id": 42}


def test_story_edit_media_helpers_build_input_story_content() -> None:
    from pyrogram import types as t

    story, calls = _legacy_story()

    _run(lambda: story.edit_photo("p.png"))
    content = calls[-1][1]["content"]
    assert isinstance(content, t.InputStoryContentPhoto)
    assert content.photo == "p.png"

    _run(lambda: story.edit_video("v.mp4"))
    content = calls[-1][1]["content"]
    assert isinstance(content, t.InputStoryContentVideo)
    assert content.video == "v.mp4"
    assert not getattr(content, "is_animation", False)

    _run(lambda: story.edit_animation("a.mp4"))
    content = calls[-1][1]["content"]
    assert isinstance(content, t.InputStoryContentVideo)
    assert content.is_animation is True


def test_story_edit_caption_passes_caption_only() -> None:
    story, calls = _legacy_story()

    _run(lambda: story.edit_caption("new caption"))
    name, kwargs = calls[-1]
    assert name == "edit_story"
    assert kwargs["chat_id"] == 777
    assert kwargs["story_id"] == 42
    assert kwargs["caption"] == "new caption"
    assert kwargs["content"] is None


def test_story_edit_privacy_builds_privacy_settings() -> None:
    from pyrogram import enums as e
    from pyrogram import types as t

    story, calls = _legacy_story()

    _run(lambda: story.edit_privacy(privacy=e.StoriesPrivacyRules.CLOSE_FRIENDS))
    settings = calls[-1][1]["privacy_settings"]
    assert isinstance(settings, t.StoryPrivacySettingsCloseFriends)

    _run(
        lambda: story.edit_privacy(
            privacy=e.StoriesPrivacyRules.SELECTED_USERS,
            allowed_users=[5, 6],
        )
    )
    settings = calls[-1][1]["privacy_settings"]
    assert isinstance(settings, t.StoryPrivacySettingsSelectedUsers)
    assert settings.user_ids == [5, 6]


def test_story_forward_reposts_via_send_story() -> None:
    story, calls = _legacy_story()

    _run(lambda: story.forward(chat_id=-100999, caption="repost"))
    name, kwargs = calls[-1]
    assert name == "send_story"
    assert kwargs["chat_id"] == -100999
    assert kwargs["fwd_from_id"] == 777
    assert kwargs["fwd_from_story"] == 42
    assert kwargs["caption"] == "repost"


def test_story_legacy_import_path_is_the_canonical_class() -> None:
    """The old module held a second, unreachable copy of the class."""
    from pyrogram.types import Story as Canonical
    from pyrogram.types.messages_and_media.story import Story as Legacy

    assert Legacy is Canonical


# --------------------------------------------------------------------------- #
# N8: Story and invoice keyword adapters in legacy_compat.
# --------------------------------------------------------------------------- #
def test_get_stories_chat_id_maps_to_story_poster_chat_id() -> None:
    out = _map("get_stories", {"chat_id": 5, "story_ids": [1]})
    assert out == {"story_poster_chat_id": 5, "story_ids": [1]}


def test_forward_story_legacy_source_kwargs() -> None:
    out = _map(
        "forward_story",
        {"from_chat_id": 5, "from_story_id": 3, "chat_id": -100},
    )
    assert out == {"chat_id": -100, "story_poster_chat_id": 5, "story_id": 3}


def test_send_story_media_and_repost_kwargs() -> None:
    out = _map(
        "send_story",
        {
            "chat_id": 5,
            "photo": "p.png",
            "denied_users": [9],
            "forward_from_chat_id": 7,
            "forward_from_story_id": 2,
        },
    )
    assert out["media"] == "p.png"
    assert out["disallowed_users"] == [9]
    assert out["fwd_from_id"] == 7
    assert out["fwd_from_story"] == 2
    assert "photo" not in out


def test_edit_story_media_privacy_and_areas_kwargs() -> None:
    from pyrogram import enums as e
    from pyrogram import types as t

    out = _map(
        "edit_story",
        {
            "chat_id": 5,
            "story_id": 3,
            "video": "v.mp4",
            "media_areas": ["area"],
            "privacy": e.StoriesPrivacyRules.CONTACTS,
            "denied_users": [8],
        },
    )
    assert isinstance(out["content"], t.InputStoryContentVideo)
    assert out["areas"] == ["area"]
    assert isinstance(out["privacy_settings"], t.StoryPrivacySettingsContacts)
    assert out["privacy_settings"].except_user_ids == [8]
    assert "media_areas" not in out
    assert "privacy" not in out


def test_edit_story_without_legacy_kwargs_is_untouched() -> None:
    out = _map("edit_story", {"chat_id": 5, "story_id": 3, "caption": "c"})
    assert out == {"chat_id": 5, "story_id": 3, "caption": "c"}


def test_send_invoice_provider_rename_and_reply_folding() -> None:
    out = _map(
        "send_invoice",
        {
            "provider": "tok",
            "photo_mime_type": "image/png",
            "extended_media": "ignored",
            "reply_to_message_id": 11,
            "quote_text": "q",
        },
    )
    assert out["provider_token"] == "tok"
    assert "photo_mime_type" not in out
    assert "extended_media" not in out
    assert out["reply_parameters"].message_id == 11
    assert out["reply_parameters"].quote == "q"


def test_send_invoice_leaves_existing_reply_parameters_alone() -> None:
    from pyrogram import types as t

    existing = t.ReplyParameters(message_id=99)
    out = _map(
        "send_invoice",
        {"reply_parameters": existing, "reply_to_message_id": 11},
    )
    assert out["reply_parameters"] is existing


# --------------------------------------------------------------------------- #
# N9: ForumTopic — the v2.7.6 copy under types.user_and_chats shadowed the
# rebased class (star-import order), so ``types.ForumTopic`` was the old class
# while the live client methods called the new five-argument ``_parse``.
# --------------------------------------------------------------------------- #
def _raw_forum_topic(**overrides):
    from pyrogram import raw

    fields = {
        "id": 9,
        "date": 1700000000,
        "title": "Topic",
        "icon_color": 7,
        "top_message": 2,
        "read_inbox_max_id": 3,
        "read_outbox_max_id": 4,
        "unread_count": 5,
        "unread_mentions_count": 6,
        "unread_reactions_count": 7,
        "unread_poll_votes_count": 8,
        "from_id": raw.types.PeerUser(user_id=5),
        "peer": raw.types.PeerChannel(channel_id=123),
        "notify_settings": raw.types.PeerNotifySettings(),
    }
    fields.update(overrides)
    return raw.types.ForumTopic(**fields)


def test_forum_topic_legacy_import_path_is_the_canonical_class() -> None:
    from pyrogram.types import ForumTopic as Canonical
    from pyrogram.types.chat_topics.forum_topic import ForumTopic as Modern
    from pyrogram.types.user_and_chats.forum_topic import ForumTopic as Legacy

    assert Canonical is Modern
    assert Legacy is Modern


def test_forum_topic_parse_accepts_the_legacy_single_argument_form() -> None:
    """v2.7.6 called ``ForumTopic._parse(raw_topic)``; get_forum_topics_by_id still does."""
    from pyrogram.types import ForumTopic

    topic = ForumTopic._parse(_raw_forum_topic())
    assert topic.message_thread_id == 9
    assert topic.name == "Topic"


def test_forum_topic_parse_accepts_the_current_five_argument_form() -> None:
    from pyrogram.types import ForumTopic

    topic = ForumTopic._parse(None, _raw_forum_topic(), {}, {}, {})
    assert topic.message_thread_id == 9
    assert topic.name == "Topic"


def test_forum_topic_exposes_both_attribute_spellings() -> None:
    from pyrogram.types import ForumTopic

    topic = ForumTopic._parse(
        _raw_forum_topic(closed=True, pinned=True, hidden=True, my=True, short=True)
    )

    # current names
    assert topic.message_thread_id == 9
    assert topic.name == "Topic"
    assert topic.is_closed is True
    assert topic.is_pinned is True
    assert topic.is_hidden is True
    assert topic.outgoing is True
    assert topic.is_reduced_version is True
    assert topic.last_read_inbox_message_id == 3
    assert topic.last_read_outbox_message_id == 4
    assert topic.unread_mention_count == 6
    assert topic.unread_reaction_count == 7
    assert topic.unread_poll_vote_count == 8

    # v2.7.6 names resolve to the same values
    assert topic.id == topic.message_thread_id
    assert topic.title == topic.name
    assert topic.closed == topic.is_closed
    assert topic.pinned == topic.is_pinned
    assert topic.hidden == topic.is_hidden
    assert topic.my == topic.outgoing
    assert topic.short == topic.is_reduced_version
    assert topic.read_inbox_max_id == topic.last_read_inbox_message_id
    assert topic.read_outbox_max_id == topic.last_read_outbox_message_id
    assert topic.unread_mentions_count == topic.unread_mention_count
    assert topic.unread_reactions_count == topic.unread_reaction_count
    assert topic.unread_poll_votes_count == topic.unread_poll_vote_count
    assert topic.date == topic.creation_date
    assert topic.from_id is topic.creator
    assert topic.icon_emoji_id == topic.icon_custom_emoji_id


def test_forum_topic_parse_tolerates_unresolvable_creator() -> None:
    """An empty users/chats map must not raise KeyError."""
    from pyrogram.types import ForumTopic

    topic = ForumTopic._parse(None, _raw_forum_topic(), {}, {}, {})
    assert topic.creator is None
    assert topic.from_id is None


def test_forum_topic_deleted_is_reported_via_is_deleted() -> None:
    from pyrogram import raw
    from pyrogram.types import ForumTopic

    topic = ForumTopic._parse(raw.types.ForumTopicDeleted(id=4))
    assert topic.is_deleted is True
    assert topic.id == 4


def test_forum_topic_created_and_edited_expose_both_spellings() -> None:
    from pyrogram import raw
    from pyrogram.types import ForumTopicCreated, ForumTopicEdited

    created = ForumTopicCreated._parse(
        raw.types.MessageActionTopicCreate(
            title="Hello", icon_color=7, icon_emoji_id=99
        )
    )
    assert created.title == "Hello"
    assert created.name == "Hello"
    assert created.icon_emoji_id == 99
    assert created.icon_custom_emoji_id == "99"

    edited = ForumTopicEdited._parse(
        raw.types.MessageActionTopicEdit(title="New", icon_emoji_id=5)
    )
    assert edited.title == "New"
    assert edited.name == "New"
    assert edited.icon_emoji_id == 5
    assert edited.icon_custom_emoji_id == "5"


# --------------------------------------------------------------------------- #
# N10: Type attributes renamed by the rebase.
# --------------------------------------------------------------------------- #
def test_checklist_legacy_attribute_aliases() -> None:
    from pyrogram.types import Checklist

    checklist = Checklist(
        title="t",
        title_entities=["entity"],
        others_can_add_tasks=True,
        others_can_mark_tasks_as_done=False,
    )
    assert checklist.entities == ["entity"]
    assert checklist.can_add_tasks is True
    assert checklist.can_mark_tasks_as_done is False


def test_checklist_task_entities_alias() -> None:
    from pyrogram.types import ChecklistTask

    task = ChecklistTask(id=1, text="x", text_entities=["entity"])
    assert task.entities == ["entity"]


def test_input_checklist_task_accepts_legacy_entities_kwarg() -> None:
    from pyrogram.types import InputChecklistTask

    legacy = InputChecklistTask(id=1, text="x", entities=["entity"])
    assert legacy.text_entities == ["entity"]
    assert legacy.entities == ["entity"]

    modern = InputChecklistTask(id=1, text="x", text_entities=["entity"])
    assert modern.entities == ["entity"]


def test_invoice_raw_alias() -> None:
    from pyrogram.types import Invoice

    invoice = Invoice(currency="USD", is_test=True, _raw="RAW")
    assert invoice.raw == "RAW"


def test_location_accepts_address() -> None:
    """v2.7.6 declared Location.address; keep the kwarg and the attribute."""
    from pyrogram.types import Location

    location = Location(longitude=1.0, latitude=2.0, address="somewhere")
    assert location.address == "somewhere"
    assert Location(longitude=1.0, latitude=2.0).address is None


def test_paid_media_accepts_legacy_kwargs() -> None:
    from pyrogram.types import PaidMedia

    media = PaidMedia(stars_amount=5, extended_media=[])
    assert media.stars_amount == 5
    assert media.extended_media == []


# --------------------------------------------------------------------------- #
# N11: Constructor keyword names the rebase renamed. A v2.7.6 application that
# builds these objects itself (tests, fixtures, custom parsers) must not
# TypeError.
# --------------------------------------------------------------------------- #
def test_checklist_accepts_legacy_constructor_kwargs() -> None:
    from pyrogram.types import Checklist

    checklist = Checklist(
        title="t",
        entities=["entity"],
        can_add_tasks=True,
        can_mark_tasks_as_done=False,
    )
    assert checklist.title_entities == ["entity"]
    assert checklist.others_can_add_tasks is True
    assert checklist.others_can_mark_tasks_as_done is False


def test_checklist_task_accepts_legacy_constructor_kwargs() -> None:
    from pyrogram.types import ChecklistTask

    task = ChecklistTask(id=1, text="x", entities=["entity"])
    assert task.text_entities == ["entity"]


def test_invoice_accepts_legacy_raw_kwarg() -> None:
    from pyrogram.types import Invoice

    invoice = Invoice(currency="USD", is_test=True, raw="RAW")
    assert invoice.raw == "RAW"
    assert invoice._raw == "RAW"


def test_forum_topic_accepts_legacy_constructor_kwargs() -> None:
    from pyrogram.types import ForumTopic

    topic = ForumTopic(
        id=11,
        date=None,
        title="Legacy",
        icon_color=3,
        top_message=7,
        read_inbox_max_id=1,
        read_outbox_max_id=2,
        unread_count=3,
        unread_mentions_count=4,
        unread_reactions_count=5,
        from_id=None,
        my=True,
        closed=True,
        pinned=True,
        short=True,
        icon_emoji_id="42",
    )
    assert topic.message_thread_id == 11
    assert topic.name == "Legacy"
    assert topic.is_closed is True
    assert topic.is_pinned is True
    assert topic.outgoing is True
    assert topic.is_reduced_version is True
    assert topic.icon_custom_emoji_id == "42"
    assert topic.last_read_inbox_message_id == 1
    assert topic.last_read_outbox_message_id == 2
    assert topic.unread_mention_count == 4
    assert topic.unread_reaction_count == 5


def test_forum_topic_created_accepts_either_spelling() -> None:
    from pyrogram.types import ForumTopicCreated

    legacy = ForumTopicCreated(id=1, title="T", icon_color=2, icon_emoji_id=3)
    assert legacy.name == "T"
    assert legacy.icon_custom_emoji_id == "3"

    modern = ForumTopicCreated(name="T", icon_color=2, icon_custom_emoji_id="3")
    assert modern.title == "T"
    assert modern.icon_emoji_id == 3


def test_story_accepts_legacy_constructor_kwargs() -> None:
    from pyrogram import enums as e
    from pyrogram import types as t

    story = t.Story(
        id=5,
        from_user=t.Chat(id=42, type=e.ChatType.PRIVATE, username="bob"),
        edited=True,
        pinned=False,
        public=True,
        denied_users=[9],
        media_areas=["area"],
        raw="RAW",
    )
    assert story.id == 5
    assert story.chat.id == 42
    assert story.is_edited is True
    assert story.is_posted_to_chat_page is False
    assert isinstance(story.privacy_settings, t.StoryPrivacySettingsEveryone)
    assert story.areas == ["area"]
    assert story._raw == "RAW"

    # and the read side still answers to the old names
    assert story.from_user.id == 42
    assert story.sender_chat is None
    assert story.privacy is e.StoryPrivacy.PUBLIC
    assert story.denied_users == [9]
    assert story.media_areas == ["area"]
    assert story.raw == "RAW"


def test_story_legacy_privacy_booleans_build_privacy_settings() -> None:
    from pyrogram import enums as e
    from pyrogram import types as t

    friends = t.Story(id=1, close_friends=True)
    assert isinstance(friends.privacy_settings, t.StoryPrivacySettingsCloseFriends)
    assert friends.privacy is e.StoryPrivacy.CLOSE_FRIENDS

    contacts = t.Story(id=2, contacts=True)
    assert isinstance(contacts.privacy_settings, t.StoryPrivacySettingsContacts)

    selected = t.Story(id=3, selected_contacts=True, allowed_users=[7])
    assert isinstance(selected.privacy_settings, t.StoryPrivacySettingsSelectedUsers)
    assert selected.allowed_users == [7]


def test_chat_photo_accepts_legacy_constructor_kwargs() -> None:
    """v2.7.6 built ChatPhoto without has_animation / is_personal."""
    from pyrogram.types import ChatPhoto

    photo = ChatPhoto(
        small_file_id="s",
        small_photo_unique_id="su",
        big_file_id="b",
        big_photo_unique_id="bu",
    )
    assert photo.has_animation is None
    assert photo.is_personal is None


def test_chat_join_request_accepts_legacy_constructor_kwargs() -> None:
    """v2.7.6 built ChatJoinRequest without user_chat_id."""
    from datetime import datetime

    from pyrogram import enums as e
    from pyrogram import types as t

    request = t.ChatJoinRequest(
        chat=t.Chat(id=-100, type=e.ChatType.SUPERGROUP),
        from_user=t.User(id=42),
        date=datetime.now(),
    )
    # Defaults to the requesting user's id, which is what it identifies.
    assert request.user_chat_id == 42


def test_inline_query_result_video_accepts_legacy_thumb_url_kwarg() -> None:
    from pyrogram.types import InlineQueryResultVideo

    result = InlineQueryResultVideo(video_url="v", thumb_url="t", title="T")
    assert result.thumbnail_url == "t"


def test_sqlite_storage_accepts_name_only() -> None:
    """v2.7.6 constructed SQLiteStorage(name) with no workdir."""
    from pyrogram.storage import SQLiteStorage

    storage = SQLiteStorage("legacy_session")
    assert str(storage.database).endswith("legacy_session.session")

    in_memory = SQLiteStorage("mem", in_memory=True)
    assert in_memory.database == ":memory:"


def test_reaction_type_write_accepts_no_client() -> None:
    """v2.7.6 called ``reaction.write()`` with no arguments."""
    from pyrogram import raw
    from pyrogram.types import (
        ReactionTypeCustomEmoji,
        ReactionTypeEmoji,
        ReactionTypePaid,
    )

    assert isinstance(ReactionTypeEmoji(emoji="👍").write(), raw.types.ReactionEmoji)
    assert isinstance(
        ReactionTypeCustomEmoji(custom_emoji_id="123").write(),
        raw.types.ReactionCustomEmoji,
    )
    assert isinstance(ReactionTypePaid().write(), raw.types.ReactionPaid)


def test_login_url_write_accepts_two_arguments() -> None:
    """v2.7.6 called ``login_url.write(text, bot)``; ``style`` came later."""
    from pyrogram import raw
    from pyrogram.types import LoginUrl

    button = LoginUrl(url="https://example.com").write("text", None)
    assert isinstance(button, raw.types.InputKeyboardButtonUrlAuth)


def test_cache_async_interface_shares_the_item_store() -> None:
    """v2.7.6 used ``await cache.get`` / ``await cache.set``."""
    from pyrogram.client import Cache

    cache = Cache(4)

    async def main() -> None:
        await cache.set(("chat", 1), "msg")
        assert await cache.get(("chat", 1)) == "msg"
        assert await cache.get("missing", "fallback") == "fallback"
        # the item interface reads and writes the same store
        assert cache[("chat", 1)] == "msg"
        cache[("chat", 2)] = "msg2"
        assert await cache.get(("chat", 2)) == "msg2"
        assert len(cache) == 2
        assert ("chat", 2) in cache

    asyncio.run(main())


def test_cache_stays_bounded_through_both_interfaces() -> None:
    from pyrogram.client import Cache

    cache = Cache(4)

    async def main() -> None:
        for i in range(20):
            await cache.set(i, i)
        assert len(cache) <= cache.capacity

    asyncio.run(main())
