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

import os
from concurrent.futures.thread import ThreadPoolExecutor


_crypto_pool = None

# Number of crypto worker threads. v2.8.6 (peak ~27 MB/s uploads) used a single
# thread: pack/unpack were serialized in order and the event loop pipelined
# cleanly against them. The multi-worker pool added in 2.8.7 dispatched every
# 512 KB part to a different thread, so N threads contended the GIL against the
# loop while the send side stayed serial (TCP.send holds a lock) — paying the
# thread-coordination cost with no parallelism gain, which halved throughput.
# Hard-reverted to 1 to match 2.8.6.
CRYPTO_WORKERS = 1


def get_crypto_executor() -> ThreadPoolExecutor:
    global _crypto_pool
    if _crypto_pool is None:
        _crypto_pool = ThreadPoolExecutor(
            max_workers=CRYPTO_WORKERS,
            thread_name_prefix="Crypto",
        )
    return _crypto_pool


def set_crypto_executor(executor: ThreadPoolExecutor):
    global _crypto_pool
    _crypto_pool = executor


def create_crypto_executor() -> ThreadPoolExecutor:
    return ThreadPoolExecutor(
        max_workers=CRYPTO_WORKERS,
        thread_name_prefix="Crypto",
    )
