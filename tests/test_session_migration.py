"""Ensure pyroblack 2.7.x .session files migrate cleanly to current schema."""

import asyncio
import sqlite3
import tempfile
from pathlib import Path

import pytest

from pyrogram.storage.sqlite_storage import SQLiteStorage

# Minimal schema matching pyroblack 2.7.2 SCHEMA + UNAME_SCHEMA (VERSION = 4)
LEGACY_27_SCHEMA = """
CREATE TABLE sessions
(
    dc_id     INTEGER PRIMARY KEY,
    api_id    INTEGER,
    test_mode INTEGER,
    auth_key  BLOB,
    date      INTEGER NOT NULL,
    user_id   INTEGER,
    is_bot    INTEGER
);

CREATE TABLE peers
(
    id             INTEGER PRIMARY KEY,
    access_hash    INTEGER,
    type           INTEGER NOT NULL,
    username       TEXT,
    phone_number   TEXT,
    last_update_on INTEGER NOT NULL DEFAULT (CAST(STRFTIME('%s', 'now') AS INTEGER))
);

CREATE TABLE update_state
(
    id   INTEGER PRIMARY KEY,
    pts  INTEGER,
    qts  INTEGER,
    date INTEGER,
    seq  INTEGER
);

CREATE TABLE version
(
    number INTEGER PRIMARY KEY
);

CREATE TABLE usernames
(
    id             TEXT PRIMARY KEY,
    peer_id        INTEGER NOT NULL,
    last_update_on INTEGER NOT NULL DEFAULT (CAST(STRFTIME('%s', 'now') AS INTEGER))
);
"""


def _make_legacy_session(path: Path) -> None:
    conn = sqlite3.connect(str(path))
    conn.executescript(LEGACY_27_SCHEMA)
    conn.execute("INSERT INTO version VALUES (4)")
    conn.execute(
        "INSERT INTO sessions VALUES (?, ?, ?, ?, ?, ?, ?)",
        (2, 12345, 0, b"\x00" * 256, 0, 111, 1),
    )
    conn.execute(
        "INSERT INTO peers (id, access_hash, type, username, phone_number) "
        "VALUES (?, ?, ?, ?, ?)",
        (111, 999, "user", "legacyuser", None),
    )
    conn.execute(
        "INSERT INTO usernames (id, peer_id) VALUES (?, ?)",
        ("legacyuser2", 222),
    )
    conn.execute(
        "INSERT INTO peers (id, access_hash, type, username, phone_number) "
        "VALUES (?, ?, ?, ?, ?)",
        (222, 888, "user", None, None),
    )
    conn.execute(
        "INSERT INTO update_state VALUES (?, ?, ?, ?, ?)",
        (0, 1, 0, 0, 0),
    )
    conn.commit()
    conn.close()


@pytest.mark.asyncio
async def test_migrate_pyroblack_2_7_session() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        workdir = Path(tmp)
        session_path = workdir / "legacy.session"
        _make_legacy_session(session_path)

        storage = SQLiteStorage("legacy", workdir=workdir)
        # Must not raise: table update_state already exists
        await storage.open()

        assert await storage.version() == SQLiteStorage.VERSION
        assert await storage.user_id() == 111
        assert await storage.api_id() == 12345

        # Modern usernames layout: id=peer_id, username=text
        peer = await storage.get_peer_by_username("legacyuser")
        assert peer.user_id == 111

        peer2 = await storage.get_peer_by_username("legacyuser2")
        assert peer2.user_id == 222

        # update_state still readable
        states = await storage.update_state()
        assert states
        assert states[0][0] == 0

        await storage.close()

        # Re-open should be idempotent
        storage2 = SQLiteStorage("legacy", workdir=workdir)
        await storage2.open()
        assert await storage2.version() == SQLiteStorage.VERSION
        await storage2.close()


def test_migrate_pyroblack_2_7_session_sync() -> None:
    """Wrapper so the test runs even if pytest-asyncio isn't configured."""
    asyncio.get_event_loop().run_until_complete(test_migrate_pyroblack_2_7_session())
