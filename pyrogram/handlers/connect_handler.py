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

from typing import Any, Callable

import pyrogram
from .handler import Handler

CallbackFunc: Callable = Callable[["pyrogram.Client", "pyrogram.session.Session"], Any]


class ConnectHandler(Handler):
    """The Connect handler class. Used to handle connections. It is intended to be used with
    :meth:`~pyrogram.Client.add_handler`

    For a nicer way to register this handler, have a look at the
    :meth:`~pyrogram.Client.on_connect` decorator.

    Parameters:
        callback (``Callable``):
            Pass a function that will be called when a connection occurs. It takes *(client, session)*
            as positional arguments.

    Other parameters:
        client (:obj:`~pyrogram.Client`):
            The Client itself.

        session (:obj:`~pyrogram.session.Session`):
            The Session used for the connection.
    """

    def __init__(self, callback: CallbackFunc):
        super().__init__(callback)
