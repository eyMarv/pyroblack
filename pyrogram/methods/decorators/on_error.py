#  Pyrogram - Telegram MTProto API Client Library for Python
#  Copyright (C) 2017-present Dan <https://github.com/delivrance>
#
#  This file is part of Pyrogram.
#
#  Pyrogram is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Lesser General Public License as published
#  by the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  Pyrogram is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public License
#  along with Pyrogram.  If not, see <http://www.gnu.org/licenses/>.

from typing import Callable, Optional, Sequence, Union

import pyrogram
from pyrogram.filters import Filter


class OnError:
    def on_error(
        self: Union["OnError", Filter, None] = None,
        exceptions: Optional[Union[Exception, Sequence[Exception]]] = None,
        filters: Optional[Filter] = None,
        group: int = 0,
    ) -> Callable:
        """Decorator for handling exceptions raised inside update handlers.

        This does the same thing as :meth:`~pyrogram.Client.add_handler` using the
        :obj:`~pyrogram.handlers.ErrorHandler`.

        Parameters:
            exceptions (``Exception`` | List of ``Exception``, *optional*):
                An exception type or a sequence of exception types that this handler should
                handle. If None, the handler will catch any exception.

            filters (:obj:`~pyrogram.filters`, *optional*):
                Pass one or more filters to allow only a subset of updates to be passed
                in your callback function.

            group (``int``, *optional*):
                The group identifier, defaults to 0.
        """

        def decorator(func: Callable) -> Callable:
            if isinstance(self, pyrogram.Client):
                self.add_handler(
                    pyrogram.handlers.ErrorHandler(func, exceptions, filters), group
                )
            elif isinstance(self, Filter) or self is None:
                if not hasattr(func, "handlers"):
                    func.handlers = []

                func.handlers.append(
                    (
                        pyrogram.handlers.ErrorHandler(func, self, exceptions),
                        group if filters is None else filters,
                    )
                )

            return func

        return decorator
