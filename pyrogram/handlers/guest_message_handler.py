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

from typing import TYPE_CHECKING, Any, Callable

from pyrogram.filters import Filter

from .handler import Handler

if TYPE_CHECKING:
    import pyrogram

CallbackFunc: Callable = Callable[
    [
        "pyrogram.Client",
        "pyrogram.types.Message",
    ],
    Any,
]


class GuestMessageHandler(Handler):
    """The Guest Message handler class. Used to handle guest messages.
    It is intended to be used with :meth:`~pyrogram.Client.add_handler`.

    For a nicer way to register this handler, have a look at the
    :meth:`~pyrogram.Client.on_guest_message` decorator.

    Parameters
    ----------
        callback (``Callable``):
            Pass a function that will be called when a new guest message arrives. It takes *(client, message)*
            as positional arguments.

        filters (:obj:`Filter`):
            Pass one or more filters to allow only a subset of messages to be passed
            in your callback function.

    Other Parameters
    ----------------
        client (:obj:`~pyrogram.Client`):
            The Client itself.

        message (:obj:`~pyrogram.types.Message`):
            The received message.

    """

    def __init__(self, callback: CallbackFunc, filters: Filter = None) -> None:
        super().__init__(callback, filters)
