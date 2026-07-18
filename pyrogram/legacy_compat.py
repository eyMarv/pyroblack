#  Pyroblack - Telegram MTProto API Client Library for Python
#  Copyright (C) 2024-present eyMarv <https://github.com/eyMarv>
#  Maintainer: irisXDR <https://github.com/irisXDR>
#
#  Compatibility wrappers so pyroblack <= 2.7.2 kwargs still work on 2.9.x.

from __future__ import annotations

import functools
import inspect
from typing import Any, Callable, Dict, Optional

# Map: method_name -> {old_kwarg: new_kwarg | None}
# None means "accept and drop" (obsolete / no longer meaningful).
# Special transforms are handled in _transform().

CLIENT_LEGACY_KWARGS: Dict[str, Dict[str, Optional[str]]] = {
    # Media caption position
    "edit_message_text": {"invert_media": None},  # text-only edit; accept no-op
    "edit_inline_text": {"invert_media": None},
    "edit_message_media": {
        # Media invert is applied on InputMedia; accept legacy kw and drop
        "invert_media": None,
        "file_name": None,
        "show_caption_above_media": None,
    },
    "edit_message_caption": {"invert_media": "show_caption_above_media"},
    "copy_message": {
        "has_spoiler": None,
        "allow_paid_broadcast": "allow_paid_broadcast",  # may already exist
    },
    # Forward
    "forward_messages": {
        "drop_author": "send_copy",
        "drop_media_captions": "remove_caption",
    },
    # Forum topics
    "close_forum_topic": {"topic_id": "message_thread_id"},
    "delete_forum_topic": {"topic_id": "message_thread_id"},
    "reopen_forum_topic": {"topic_id": "message_thread_id"},
    "edit_forum_topic": {
        "topic_id": "message_thread_id",
        "title": "name",
        "icon_emoji_id": "icon_custom_emoji_id",
    },
    "create_forum_topic": {
        "title": "name",
        "icon_emoji_id": "icon_custom_emoji_id",
    },
    "get_forum_topics": {
        "offset_topic": "offset_id",
        "offset_id": "offset_id",
    },
    # Search / messages
    "search_messages": {"thread_id": "message_thread_id"},
    "search_messages_count": {"thread_id": "message_thread_id"},
    "get_messages": {"reply_to_message_ids": "message_ids"},
    # Dialogs
    "get_dialogs": {
        "from_archive": None,  # use chat_list=1 instead; transformed below
        "exclude_pinned": None,
    },
    "get_dialogs_count": {"from_archive": None},
    # Payments
    "answer_pre_checkout_query": {
        "success": "ok",
        "error": "error_message",
    },
    # get_payment_form / send_payment_form accept chat_id+message_id natively
    # (dual API with modern input_invoice) — do not strip those kwargs.
    # Promote
    "promote_chat_member": {"title": None},  # custom title set via privileges / separate API
    # Poll
    "send_poll": {
        "correct_option_id": None,  # transformed -> correct_option_ids
        "explanation_parse_mode": "parse_mode",
        "explanation_entities": None,
        "question_entities": None,
        "parse_mode": "parse_mode",
        "reply_to_message_id": None,  # transformed via reply_parameters if needed
    },
    # Misc
    "send_reaction": {"story_id": "story_id", "emoji": "emoji", "big": "big"},
    "send_contact": {"parse_mode": None},
    "send_dice": {"parse_mode": None},
    "send_location": {"parse_mode": None},
    "send_venue": {"parse_mode": None},
    "send_inline_bot_result": {
        "parse_mode": None,
        "quote_text": "quote_text",
        "quote_entities": "quote_entities",
    },
    "send_media_group": {
        "parse_mode": None,
        "progress": None,
        "progress_args": None,
    },
    "export_chat_invite_link": {
        "subscription_period": None,
        "subscription_price": None,
    },
    "set_chat_photo": {
        "emoji": None,
        "emoji_background": None,
        "video_start_ts": "video_start_timestamp",
    },
    "set_profile_photo": {
        "emoji": None,
        "emoji_background": None,
        "is_public": None,
    },
    "translate_message_text": {
        "text": None,
        "entities": None,
        "parse_mode": None,
    },
    "send_code": {
        "current_number": None,
        "allow_flashcall": None,
        "allow_missed_call": None,
        "allow_app_hash": None,
        "allow_firebase": None,
        "logout_tokens": None,
        "token": None,
        "app_sandbox": None,
    },
}

MESSAGE_LEGACY_KWARGS: Dict[str, Dict[str, Optional[str]]] = {
    "edit_text": {
        "invert_media": None,
        "business_connection_id": "business_connection_id",
    },
    "edit_caption": {
        "invert_media": "show_caption_above_media",
        "business_connection_id": "business_connection_id",
    },
    "edit_media": {
        "invert_media": "show_caption_above_media",
        "business_connection_id": "business_connection_id",
    },
    "edit_reply_markup": {"business_connection_id": "business_connection_id"},
    "forward": {
        "drop_author": "send_copy",
        "drop_media_captions": "remove_caption",
    },
    "copy": {
        "has_spoiler": None,
        "invert_media": "show_caption_above_media",
        "quote_text": "quote_text",
        "quote_entities": "quote_entities",
        "reply_to_chat_id": "reply_to_chat_id",
    },
    "react": {"big": "big", "emoji": "emoji"},
}


def _transform(method_name: str, kwargs: dict) -> dict:
    """Apply special-case transforms after simple renames."""
    # from_archive=True  -> chat_list=1 (archive)
    if method_name in ("get_dialogs", "get_dialogs_count"):
        if kwargs.pop("from_archive", None):
            kwargs.setdefault("chat_list", 1)

    # send_poll: correct_option_id (int) -> correct_option_ids (list)
    if method_name == "send_poll":
        coid = kwargs.pop("correct_option_id", None)
        if coid is not None and "correct_option_ids" not in kwargs:
            kwargs["correct_option_ids"] = [coid] if not isinstance(coid, list) else coid
        # reply_to_message_id -> reply_parameters if needed
        rmid = kwargs.pop("reply_to_message_id", None)
        if rmid is not None and kwargs.get("reply_parameters") is None:
            try:
                from pyrogram import types
                kwargs["reply_parameters"] = types.ReplyParameters(message_id=rmid)
            except Exception:
                pass
        # drop unused entity kwargs if explanation is plain str (best-effort)
        kwargs.pop("explanation_entities", None)
        kwargs.pop("question_entities", None)

    # get_messages: reply_to_message_ids was an alternate name for message_ids
    if method_name == "get_messages":
        rids = kwargs.pop("reply_to_message_ids", None)
        if rids is not None and kwargs.get("message_ids") is None:
            kwargs["message_ids"] = rids

    # invert_media on caption edits -> show_caption_above_media
    if "invert_media" in kwargs and "show_caption_above_media" not in kwargs:
        # only when target method accepts show_caption_above_media (handled by alias map)
        pass

    return kwargs


def _wrap_method(func: Callable, method_name: str, aliases: Dict[str, Optional[str]]) -> Callable:
    if getattr(func, "_legacy_kwargs_wrapped", False):
        return func

    is_coro = inspect.iscoroutinefunction(func)
    is_async_gen = inspect.isasyncgenfunction(func)

    if is_async_gen:
        @functools.wraps(func)
        async def agen_wrapper(self, *args, **kwargs):
            kwargs = _apply_aliases(kwargs, aliases)
            kwargs = _transform(method_name, kwargs)
            async for item in func(self, *args, **kwargs):
                yield item

        agen_wrapper._legacy_kwargs_wrapped = True  # type: ignore[attr-defined]
        agen_wrapper.__signature__ = _open_signature(func)  # type: ignore[attr-defined]
        return agen_wrapper

    if is_coro:
        @functools.wraps(func)
        async def async_wrapper(self, *args, **kwargs):
            kwargs = _apply_aliases(kwargs, aliases)
            kwargs = _transform(method_name, kwargs)
            result = func(self, *args, **kwargs)
            # Some methods are annotated/async but return async generators via return
            if inspect.isasyncgen(result):
                return result
            return await result

        async_wrapper._legacy_kwargs_wrapped = True  # type: ignore[attr-defined]
        # Accept any kwargs at call time (override signature binding)
        async_wrapper.__signature__ = _open_signature(func)  # type: ignore[attr-defined]
        return async_wrapper

    @functools.wraps(func)
    def sync_wrapper(self, *args, **kwargs):
        kwargs = _apply_aliases(kwargs, aliases)
        kwargs = _transform(method_name, kwargs)
        return func(self, *args, **kwargs)

    sync_wrapper._legacy_kwargs_wrapped = True  # type: ignore[attr-defined]
    sync_wrapper.__signature__ = _open_signature(func)  # type: ignore[attr-defined]
    return sync_wrapper


def _apply_aliases(kwargs: dict, aliases: Dict[str, Optional[str]]) -> dict:
    out = dict(kwargs)
    for old, new in aliases.items():
        if old not in out:
            continue
        val = out.pop(old)
        if new is None:
            continue
        if new not in out:
            out[new] = val
    return out


def _open_signature(func: Callable) -> inspect.Signature:
    """Return a signature that accepts **kwargs so old names don't TypeError."""
    try:
        sig = inspect.signature(func)
    except (TypeError, ValueError):
        return inspect.Signature(
            [
                inspect.Parameter("self", inspect.Parameter.POSITIONAL_OR_KEYWORD),
                inspect.Parameter("args", inspect.Parameter.VAR_POSITIONAL),
                inspect.Parameter("kwargs", inspect.Parameter.VAR_KEYWORD),
            ]
        )
    params = list(sig.parameters.values())
    if not any(p.kind == inspect.Parameter.VAR_KEYWORD for p in params):
        params.append(
            inspect.Parameter("kwargs", inspect.Parameter.VAR_KEYWORD)
        )
    return sig.replace(parameters=params)


def install_legacy_kwargs() -> None:
    """Patch Client and Message methods to accept pyroblack <= 2.7.2 kwargs."""
    from pyrogram.client import Client
    from pyrogram.types.messages_and_media.message import Message

    for name, aliases in CLIENT_LEGACY_KWARGS.items():
        # Walk MRO to find the defining class and patch there + Client
        for cls in Client.__mro__:
            if name in cls.__dict__:
                orig = cls.__dict__[name]
                if callable(orig):
                    wrapped = _wrap_method(orig, name, aliases)
                    setattr(cls, name, wrapped)
                break
        else:
            # still try setattr on Client if exists via descriptor
            orig = getattr(Client, name, None)
            if callable(orig):
                setattr(Client, name, _wrap_method(orig, name, aliases))

    for name, aliases in MESSAGE_LEGACY_KWARGS.items():
        if name in Message.__dict__:
            orig = Message.__dict__[name]
            if callable(orig):
                setattr(Message, name, _wrap_method(orig, name, aliases))

    # reply_* methods: bulk map common legacy kwargs
    reply_aliases = {
        "reply_in_chat_id": None,  # transformed separately if needed
        "business_connection_id": "business_connection_id",
        "invert_media": "show_caption_above_media",
        "quote_text": "quote_text",
        "quote_entities": "quote_entities",
        "parse_mode": "parse_mode",
        "correct_option_id": None,
        "explanation_parse_mode": None,
        "explanation_entities": None,
        "progress": None,
        "progress_args": None,
    }
    for name, obj in list(Message.__dict__.items()):
        if not name.startswith("reply_") or not callable(obj):
            continue
        if getattr(obj, "_legacy_kwargs_wrapped", False):
            continue
        setattr(Message, name, _wrap_method(obj, name, reply_aliases))
