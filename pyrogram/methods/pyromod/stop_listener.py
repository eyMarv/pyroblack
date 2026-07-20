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

import inspect
from typing import TYPE_CHECKING

from pyrogram.errors import ListenerStopped
from pyrogram.types import Listener
from pyrogram.utils import PyromodConfig

if TYPE_CHECKING:
    import pyrogram


class StopListener:
    async def stop_listener(self: "pyrogram.Client", listener: Listener) -> None:
        """Stops a listener, calling stopped_handler if applicable or raising ListenerStopped if throw_exceptions is True.

        .. include:: /_includes/usable-by/users-bots.rst

        Parameters
        ----------
            listener (:obj:`~pyrogram.types.Listener`):
                The listener to remove.

        Raises
        ------
            ListenerStopped: If throw_exceptions is True.

        """
        self.remove_listener(listener)

        if listener.future.done():
            return

        if callable(PyromodConfig.stopped_handler):
            if inspect.iscoroutinefunction(PyromodConfig.stopped_handler.__call__):
                await PyromodConfig.stopped_handler(None, listener)
            else:
                await self.loop.run_in_executor(
                    None,
                    PyromodConfig.stopped_handler,
                    None,
                    listener,
                )
        elif PyromodConfig.throw_exceptions:
            listener.future.set_exception(ListenerStopped())
