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

"""Bounded in-flight accounting for media downloads.

Every ``upload.GetFile`` response materializes a full chunk (up to 1 MiB)
in process memory. With many concurrent streams, uncontrolled buffering
is what actually drives RSS — not the number of open connections.

:class:`ByteBudget` caps the *total* bytes that may be in-flight or
buffered at any moment, across every :class:`~pyrogram.Client` in the
process. Fetchers block on :meth:`ByteBudget.acquire` once the budget is
exhausted, so downloads degrade into queueing instead of memory growth.
"""

from __future__ import annotations

import asyncio


class ByteBudget:
    """Async byte-counting semaphore shared across clients and streams.

    ``total`` is the maximum number of bytes allowed to be checked out at
    once. A ``total`` of 0 disables the budget entirely: every acquire
    passes through immediately.
    """

    def __init__(self, total: int = 0) -> None:
        self._total = max(0, int(total))
        self._used = 0
        self._cond: asyncio.Condition | None = None

    def _condition(self) -> asyncio.Condition:
        # Created lazily so a budget instantiated before the loop starts
        # (e.g. at import/config time) never binds to the wrong loop.
        if self._cond is None:
            self._cond = asyncio.Condition()
        return self._cond

    async def acquire(self, n: int) -> int:
        """Reserve ``n`` bytes, waiting until they fit the budget.

        Returns the amount actually granted (``min(n, total)``) so a
        request larger than the whole budget still proceeds alone rather
        than deadlocking.
        """
        granted = min(int(n), self._total)
        if granted <= 0:
            return 0
        cond = self._condition()
        async with cond:
            while self._used + granted > self._total:
                await cond.wait()
            self._used += granted
        return granted

    async def release(self, n: int) -> None:
        """Return ``n`` bytes to the budget."""
        if n <= 0:
            return
        cond = self._condition()
        async with cond:
            self._used = max(0, self._used - int(n))
            cond.notify_all()

    def set_total(self, total: int) -> None:
        """Resize the budget. Safe while transfers are running: shrinking
        below current usage just makes new acquires wait until usage
        drains under the new cap."""
        self._total = max(0, int(total))

    @property
    def total(self) -> int:
        return self._total

    @property
    def used(self) -> int:
        return self._used


_default_budget = ByteBudget(0)


def get_download_budget() -> ByteBudget:
    """Return the process-wide download budget shared by all clients."""
    return _default_budget


def set_download_budget(total_bytes: int) -> ByteBudget:
    """Resize the process-wide download budget.

    Call once at startup (before starting clients), or pass
    ``download_budget_bytes`` to the :class:`~pyrogram.Client`
    constructor — both configure the same shared instance.
    """
    _default_budget.set_total(total_bytes)
    return _default_budget
