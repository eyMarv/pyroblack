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

from __future__ import annotations

from typing import TYPE_CHECKING

import pyrogram
from pyrogram import raw, types, utils
from pyrogram.types.object import Object

if TYPE_CHECKING:
    from datetime import datetime


class ForumTopic(Object):
    """This object represents a forum topic.

    Parameters
    ----------
        message_thread_id (``int``):
            Unique identifier of the forum topic

        name (``str``):
            Name of the topic

        icon_color  (``int``):
            Color of the topic icon in RGB format

        icon_custom_emoji_id (``str``, *optional*):
            Unique identifier of the custom emoji shown as the topic icon

        is_name_implicit (``bool``, *optional*):
            True, if the name of the topic wasn't specified explicitly by its creator and likely needs to be changed by the bot.

        creation_date (:py:obj:`~datetime.datetime`, *optional*):
            Point in time (Unix timestamp) when the topic was created

        creator (:obj:`~pyrogram.types.Chat`, *optional*):
            Identifier of the creator of the topic

        outgoing (``bool``, *optional*):
            True, if the topic was created by the current user

        is_closed (``bool``, *optional*):
            True, if the topic is closed

        is_hidden (``bool``, *optional*):
            True, if the topic is hidden above the topic list and closed; for General topic only

        is_deleted (``bool``, *optional*):
            True, if the topic is delete

        last_message (:obj:`~pyrogram.types.Message`, *optional*):
            Last message in the topic; may be None if unknown

        is_pinned (``bool``, *optional*):
            True, if the topic is pinned

        unread_count (``int``, *optional*):
            Number of unread messages in the topic

        last_read_inbox_message_id (``int``, *optional*):
            Identifier of the last read incoming message

        last_read_outbox_message_id (``int``, *optional*):
            Identifier of the last read outgoing message

        unread_mention_count (``int``, *optional*):
            Number of unread messages with a mention/reply in the topic

        unread_reaction_count (``int``, *optional*):
            Number of messages with unread reactions in the topic

        unread_poll_vote_count (``int``, *optional*):
            Number of messages with unread poll votes in the topic.

        is_reduced_version (``bool``, *optional*):
            True, if this is a reduced version of the full topic information.
            If needed, full information can be fetched using :meth:`~pyrogram.Client.get_forum_topic`.

    """

    def __init__(
        self,
        *,
        message_thread_id: int | None = None,
        name: str | None = None,
        icon_color: int | None = None,
        icon_custom_emoji_id: str | None = None,
        is_name_implicit: bool | None = None,
        creation_date: datetime | None = None,
        creator: types.Chat = None,
        outgoing: bool | None = None,
        is_closed: bool | None = None,
        is_hidden: bool | None = None,
        is_deleted: bool | None = None,
        last_message: types.Message = None,
        is_pinned: bool | None = None,
        unread_count: int | None = None,
        last_read_inbox_message_id: int | None = None,
        last_read_outbox_message_id: int | None = None,
        unread_mention_count: int | None = None,
        unread_reaction_count: int | None = None,
        unread_poll_vote_count: int | None = None,
        is_reduced_version: bool | None = None,
        # pyroblack <= 2.7.6 keyword names. Accepted so the old constructor call
        # binds; each feeds the corresponding field above, and the read-side
        # aliases (properties, further down) map back the other way.
        id: int | None = None,
        title: str | None = None,
        date: datetime | None = None,
        from_id: types.Chat = None,
        top_message: int | None = None,
        my: bool | None = None,
        closed: bool | None = None,
        hidden: bool | None = None,
        pinned: bool | None = None,
        short: bool | None = None,
        icon_emoji_id: str | None = None,
        read_inbox_max_id: int | None = None,
        read_outbox_max_id: int | None = None,
        unread_mentions_count: int | None = None,
        unread_reactions_count: int | None = None,
        unread_poll_votes_count: int | None = None,
    ) -> None:
        super().__init__()

        def pick(new, old):
            return new if new is not None else old

        message_thread_id = pick(message_thread_id, id)
        name = pick(name, title)
        creation_date = pick(creation_date, date)
        creator = pick(creator, from_id)
        outgoing = pick(outgoing, my)
        is_closed = pick(is_closed, closed)
        is_hidden = pick(is_hidden, hidden)
        is_pinned = pick(is_pinned, pinned)
        is_reduced_version = pick(is_reduced_version, short)
        icon_custom_emoji_id = pick(icon_custom_emoji_id, icon_emoji_id)
        last_read_inbox_message_id = pick(last_read_inbox_message_id, read_inbox_max_id)
        last_read_outbox_message_id = pick(
            last_read_outbox_message_id, read_outbox_max_id
        )
        unread_mention_count = pick(unread_mention_count, unread_mentions_count)
        unread_reaction_count = pick(unread_reaction_count, unread_reactions_count)
        unread_poll_vote_count = pick(unread_poll_vote_count, unread_poll_votes_count)
        # ``top_message`` was the id of the topic's last message; ``last_message``
        # holds the message itself now, so the bare id has nowhere to live and is
        # recovered from ``last_message`` by the property below.
        del top_message

        self.message_thread_id = message_thread_id
        self.name = name
        self.icon_color = icon_color
        self.icon_custom_emoji_id = icon_custom_emoji_id
        self.is_name_implicit = is_name_implicit
        self.creation_date = creation_date
        self.creator = creator
        self.outgoing = outgoing
        # self.is_general = is_general
        self.is_closed = is_closed
        self.is_hidden = is_hidden
        self.is_deleted = is_deleted
        self.last_message = last_message
        self.is_pinned = is_pinned
        self.unread_count = unread_count
        self.last_read_inbox_message_id = last_read_inbox_message_id
        self.last_read_outbox_message_id = last_read_outbox_message_id
        self.unread_mention_count = unread_mention_count
        self.unread_reaction_count = unread_reaction_count
        self.unread_poll_vote_count = unread_poll_vote_count

        self.is_reduced_version = is_reduced_version

    # ------------------------------------------------------------------
    # pyroblack <= 2.7.6 attribute names.
    #
    # The rebase renamed every field on this class to the Bot API spelling.
    # These read-only aliases keep the old names resolving; there is one stored
    # value per field, so the two spellings can never disagree.
    # ------------------------------------------------------------------

    @property
    def id(self) -> int:
        """Deprecated alias of :attr:`message_thread_id`."""
        return self.message_thread_id

    @property
    def title(self) -> str:
        """Deprecated alias of :attr:`name`."""
        return self.name

    @property
    def icon_emoji_id(self) -> str | None:
        """Deprecated alias of :attr:`icon_custom_emoji_id`."""
        return self.icon_custom_emoji_id

    @property
    def date(self) -> datetime | None:
        """Deprecated alias of :attr:`creation_date`.

        v2.7.6 exposed a raw unix timestamp here; this returns the
        :class:`~datetime.datetime` that :attr:`creation_date` holds.
        """
        return self.creation_date

    @property
    def from_id(self) -> types.Chat | None:
        """Deprecated alias of :attr:`creator`.

        v2.7.6 returned a ``PeerUser``/``PeerChannel``; this returns the
        :obj:`~pyrogram.types.Chat` that :attr:`creator` holds, so ``.id``
        resolves the same way.
        """
        return self.creator

    @property
    def top_message(self) -> int | None:
        """Deprecated: id of the topic's last message (see :attr:`last_message`)."""
        return getattr(self.last_message, "id", None)

    @property
    def my(self) -> bool | None:
        """Deprecated alias of :attr:`outgoing`."""
        return self.outgoing

    @property
    def closed(self) -> bool | None:
        """Deprecated alias of :attr:`is_closed`."""
        return self.is_closed

    @property
    def hidden(self) -> bool | None:
        """Deprecated alias of :attr:`is_hidden`."""
        return self.is_hidden

    @property
    def pinned(self) -> bool | None:
        """Deprecated alias of :attr:`is_pinned`."""
        return self.is_pinned

    @property
    def short(self) -> bool | None:
        """Deprecated alias of :attr:`is_reduced_version`."""
        return self.is_reduced_version

    @property
    def read_inbox_max_id(self) -> int | None:
        """Deprecated alias of :attr:`last_read_inbox_message_id`."""
        return self.last_read_inbox_message_id

    @property
    def read_outbox_max_id(self) -> int | None:
        """Deprecated alias of :attr:`last_read_outbox_message_id`."""
        return self.last_read_outbox_message_id

    @property
    def unread_mentions_count(self) -> int | None:
        """Deprecated alias of :attr:`unread_mention_count`."""
        return self.unread_mention_count

    @property
    def unread_reactions_count(self) -> int | None:
        """Deprecated alias of :attr:`unread_reaction_count`."""
        return self.unread_reaction_count

    @property
    def unread_poll_votes_count(self) -> int | None:
        """Deprecated alias of :attr:`unread_poll_vote_count`."""
        return self.unread_poll_vote_count

    @staticmethod
    def _parse(
        client: pyrogram.Client = None,
        forum_topic: raw.base.ForumTopic = None,
        messages: dict | None = None,  # friendly
        users: dict | None = None,  # raw
        chats: dict | None = None,  # raw
    ) -> ForumTopic:
        # pyroblack <= 2.7.6 called this as ``_parse(forum_topic)``. Both call
        # forms are still live in-tree (``get_forum_topics_by_id`` uses the short
        # one, ``chat_event`` the long one), so accept either: if the first
        # argument is a raw topic rather than a Client, shift it into place.
        if forum_topic is None and client is not None:
            client, forum_topic = None, client

        messages = messages or {}
        users = users or {}
        chats = chats or {}

        if not forum_topic:
            return None

        if isinstance(forum_topic, raw.types.ForumTopicDeleted):
            return ForumTopic(
                message_thread_id=forum_topic.id,
                name=None,
                icon_color=None,
                is_deleted=True,
            )

        creator = None
        peer = getattr(forum_topic, "from_id", None)
        if peer:
            peer_id = utils.get_raw_peer_id(peer)
            if isinstance(peer, raw.types.PeerUser):
                if peer_id in users:
                    creator = types.Chat._parse_user_chat(client, users[peer_id])
            elif peer_id in chats:
                creator = types.Chat._parse_channel_chat(client, chats[peer_id])

        last_message = None
        top_message_id = getattr(forum_topic, "top_message", None)
        if top_message_id:
            last_message = messages.get(top_message_id)

        return ForumTopic(
            message_thread_id=forum_topic.id,
            name=forum_topic.title,
            icon_color=forum_topic.icon_color,  # TODO
            icon_custom_emoji_id=forum_topic.icon_emoji_id,
            is_name_implicit=forum_topic.title_missing,
            creation_date=utils.timestamp_to_datetime(forum_topic.date),
            creator=creator,
            outgoing=forum_topic.my,
            is_closed=forum_topic.closed,
            is_hidden=forum_topic.hidden,
            last_message=last_message,
            is_pinned=forum_topic.pinned,
            unread_count=forum_topic.unread_count,
            last_read_inbox_message_id=forum_topic.read_inbox_max_id,
            last_read_outbox_message_id=forum_topic.read_outbox_max_id,
            unread_mention_count=forum_topic.unread_mentions_count,
            unread_reaction_count=forum_topic.unread_reactions_count,
            unread_poll_vote_count=forum_topic.unread_poll_votes_count,
            # TODO: notify_settings: PeerNotifySettings, draft: DraftMessage
            is_reduced_version=forum_topic.short,
        )
