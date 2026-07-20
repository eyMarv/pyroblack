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

from collections.abc import Sequence
from typing import TYPE_CHECKING, Any, Callable

from .handler import Handler

if TYPE_CHECKING:
    from pyrogram.filters import Filter


class ErrorHandler(Handler):
    """The Error handler class. Used to handle unexpected errors.

    It is intended to be used with :meth:`~pyrogram.Client.add_handler`.

    For a more convenient way to register this handler, see the
    :meth:`~pyrogram.Client.on_error` decorator.

    Parameters
    ----------
        callback (``Callable``):
            A function that will be called whenever an unexpected error is raised.

        exceptions (``Exception`` | List of ``Exception``, *optional*):
            An exception type or a sequence of exception types that this handler should handle.
            If None, the handler will catch any exception that is a subclass of ``Exception``.

        filters (:obj:`Filter`, *optional*):
            Pass one or more filters to allow only a subset of updates to be passed
            in your callback function.

    """

    def __init__(
        self,
        callback: Callable[..., Any],
        exceptions: type | Sequence[type] | None = None,
        filters: Filter | None = None,
    ) -> None:
        super().__init__(callback, filters)

        if exceptions is None:
            self.exceptions = (Exception,)
        elif isinstance(exceptions, Sequence):
            self.exceptions = tuple(exceptions)
        else:
            self.exceptions = (exceptions,)
