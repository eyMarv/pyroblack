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

from dataclasses import dataclass


@dataclass
class Identifier:
    """A dataclass for matching listeners to update data.

    Parameters
    ----------
        inline_message_id (``str`` | Iterable of ``str``, *optional*):
            The inline message ID to match.
            If None, it is not considered for matching.

        chat_id (``int`` | ``str`` | Iterable, *optional*):
            The chat ID to match.
            If None, it is not considered for matching.

        message_id (``int`` | Iterable of ``int``):
            The message ID to match.
            If None, it is not considered for matching.

        from_user_id (``int`` | ``str`` | Iterable, *optional*):
            The user ID to match.
            If None, it is not considered for matching.

    """

    inline_message_id: str | list[str] | None = None
    chat_id: int | str | list[int | str] | None = None
    message_id: int | list[int] | None = None
    from_user_id: int | str | list[int | str] | None = None

    def matches(self, update: Identifier) -> bool:
        """Check if an update matches this identifier's pattern."""
        for field in type(self).__annotations__:
            pattern_value = getattr(self, field)
            update_value = getattr(update, field)

            if pattern_value is not None:
                if isinstance(update_value, list):
                    if isinstance(pattern_value, list):
                        if not set(update_value).intersection(set(pattern_value)):
                            return False
                    elif pattern_value not in update_value:
                        return False
                elif isinstance(pattern_value, list):
                    if update_value not in pattern_value:
                        return False
                elif update_value != pattern_value:
                    return False
        return True

    def count_populated(self) -> int:
        """Count how many fields are set (non-None)."""
        non_null_count = 0

        for attr in type(self).__annotations__:
            if getattr(self, attr) is not None:
                non_null_count += 1

        return non_null_count
