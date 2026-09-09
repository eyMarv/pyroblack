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

import logging
from typing import TYPE_CHECKING

from .sqlite_storage import SQLiteStorage

if TYPE_CHECKING:
    from pathlib import Path

log = logging.getLogger(__name__)

# pyroblack <= 2.7.6 defined this here and ran it during its v4 -> v5 migration.
# The table is part of ``sqlite_storage.SCHEMA`` now, so the script is kept only
# for third-party storage backends that imported it. Made idempotent (``IF NOT
# EXISTS``) so re-running it against a current session file is a no-op rather
# than "table update_state already exists".
# language=SQLite
UPDATE_STATE_SCHEMA = """
CREATE TABLE IF NOT EXISTS update_state
(
    id   INTEGER PRIMARY KEY,
    pts  INTEGER,
    qts  INTEGER,
    date INTEGER,
    seq  INTEGER
);
"""


class FileStorage(SQLiteStorage):
    """File-based session storage (backward-compatible alias for SQLiteStorage).

    Sessions are stored as ``<name>.session`` files using the standard
    pyrogram / PyroTGFork SQLite schema, so existing .session files
    from any Pyrogram-family fork can be loaded directly.
    """

    FILE_EXTENSION = ".session"

    def __init__(
        self,
        name: str,
        workdir: Path,
        session_string: str | None = None,
        is_telethon_string: bool = False,
    ) -> None:
        super().__init__(
            name,
            workdir=workdir,
            session_string=session_string,
            is_telethon_string=is_telethon_string,
            in_memory=False,
        )

    # Explicit wrappers so v2.7.2 call sites / AST see these on FileStorage
    async def open(self):
        return await super().open()

    async def delete(self):
        return await super().delete()

    async def update(self):
        return await super().update()
