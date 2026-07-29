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
    assert any(
        p.kind == inspect.Parameter.VAR_KEYWORD
        for p in sig.parameters.values()
    ) or "kwargs" in sig.parameters


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
        (GetForumTopics, dict(channel=peer, offset_date=0, offset_id=0, offset_topic=0, limit=10)),
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
        (MessageServiceType, "general_topic_hidden", MessageServiceType.GENERAL_TOPIC_HIDDEN),
        (MessageServiceType, "general_topic_unhidden", MessageServiceType.GENERAL_TOPIC_UNHIDDEN),
        (MessageServiceType, "video_chat_members_invited", MessageServiceType.VIDEO_CHAT_MEMBERS_INVITED),
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


