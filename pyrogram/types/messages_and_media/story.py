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

``Story`` moved to :mod:`pyrogram.types.stories.story` during the rebase. This
module used to hold a full second copy of the class, which was a hazard: nothing
imported it, its constructor no longer matched what the parsers produce, and
``isinstance(story, ...)`` against it was always false, because the object the
client hands you is the ``types.stories`` class. It re-exports the canonical
class now.

The v2.7.6 attributes and bound methods (``reply_*``, ``edit_*``, ``delete``,
``forward``, ``export_link``, ``from_user``, ``sender_chat``, ``privacy``, …) are
provided on that class by
:class:`~pyrogram.types.stories.story_compat.LegacyStoryMixin`, so code written
against this import path keeps working.
"""

from __future__ import annotations

from pyrogram.types.stories.story import Story

__all__ = ["Story"]
