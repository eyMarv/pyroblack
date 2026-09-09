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

"""Import location kept for pyroblack <= 2.7.6.

``ForumTopic`` moved to :mod:`pyrogram.types.chat_topics.forum_topic` during the
rebase. This module held a second copy of the class, and because
``pyrogram/types/__init__.py`` star-imports ``user_and_chats`` *after*
``chat_topics``, that copy shadowed the real one — so ``types.ForumTopic`` was
the v2.7.6 class while :meth:`~pyrogram.Client.get_forum_topics` and
:meth:`~pyrogram.Client.get_forum_topic` called the new five-argument
``_parse``. Listing topics raised ``TypeError: _parse() takes 1 positional
argument but 5 were given``.

It re-exports the canonical class now. That class carries the v2.7.6 attribute
names (``id``, ``title``, ``date``, ``closed``, ``pinned``, ``icon_emoji_id``, …)
as read-only aliases, and its ``_parse`` accepts both the old one-argument and
the new five-argument call forms.

One behavioural difference remains: parsing a deleted topic yields a
``ForumTopic`` with ``is_deleted=True`` rather than a separate
:obj:`~pyrogram.types.ForumTopicDeleted`. The ``ForumTopicDeleted`` class is
still exported, so imports keep working, but ``isinstance`` checks against it no
longer match — test ``topic.is_deleted`` instead.
"""

from __future__ import annotations

from pyrogram.types.chat_topics.forum_topic import ForumTopic

__all__ = ["ForumTopic"]
