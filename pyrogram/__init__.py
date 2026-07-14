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

__fork_name__ = "pyroblack"
__version__ = "2.9.0"
__license__ = "GNU Lesser General Public License v3.0 (LGPL-3.0)"
__copyright__ = "#  Copyright (C) 2024-present eyMarv <https://github.com/eyMarv>"

class StopTransmission(Exception):
    pass


class StopPropagation(StopAsyncIteration):
    pass


class ContinuePropagation(StopAsyncIteration):
    pass


from . import raw, types, filters, handlers, emoji, enums
from .client import Client
from .sync import idle, compose
from .crypto.executor import get_crypto_executor

# Multi-worker crypto pool (cpu_count workers). Replaces the old single-thread
# ThreadPoolExecutor(1) which serialized all AES work under multi-session load.
# Keep the public name `crypto_executor` for backward compatibility with any
# code that imported it.
crypto_executor = get_crypto_executor()
