#  pyroblack - Telegram MTProto API Client Library for Python
#  Copyright (C) 2017-present Dan <https://github.com/delivrance>
#  Copyright (C) 2024-present eyMarv <https://github.com/eyMarv>
#
#  This file is part of pyroblack.
#
#  pyroblack is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Lesser General Public License as published
#  by the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  pyroblack is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public License
#  along with pyroblack.  If not, see <http://www.gnu.org/licenses/>.

import logging
from pathlib import Path

from .sqlite_storage import SQLiteStorage

log = logging.getLogger(__name__)


class MemoryStorage(SQLiteStorage):
    """In-memory session storage (backward-compatible alias for SQLiteStorage).

    Sessions live in an ``:memory:`` SQLite database and are discarded
    when the client stops — exactly like the old aiosqlite-based version.
    """

    def __init__(
        self,
        name: str,
        session_string: str = None,
        is_telethon_string: bool = False,
    ):
        super().__init__(
            name,
            workdir=Path("."),  # unused for in-memory
            session_string=session_string,
            is_telethon_string=is_telethon_string,
            in_memory=True,
        )
