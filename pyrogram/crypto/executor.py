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

"""Shared crypto thread pool.

* **TgCrypto-pyroblack** with ``pack_message`` / ``unpack_message`` releases the
  GIL for the whole MTProto frame → ``cpu_count`` workers (true parallel crypto
  across media sessions).
* Pure-Python crypto holds the GIL → keep **1** worker.
"""

import os
from concurrent.futures.thread import ThreadPoolExecutor

_crypto_pool = None


def _has_native_mtproto() -> bool:
    try:
        import tgcrypto

        return hasattr(tgcrypto, "pack_message") and hasattr(
            tgcrypto, "unpack_message"
        )
    except ImportError:
        return False


CRYPTO_WORKERS = max(1, (os.cpu_count() or 4)) if _has_native_mtproto() else 1


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
