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
from pyrogram.filters import Filter

from .handler import Handler

CallbackFunc: Callable = Callable[
    [
        "pyrogram.Client",
        pyrogram.types.ChosenInlineResult,
    ],
    Any,
]


class ChosenInlineResultHandler(Handler):
    """The ChosenInlineResultHandler handler class. Used to handle chosen inline results coming from inline queries.
    It is intended to be used with :meth:`~pyrogram.Client.add_handler`.

    Please see the official documentation on the `feedback collecting <https://core.telegram.org/bots/inline#collecting-feedback>`_ for details on how to enable these updates for your bot.

    `This should only be used for statistical purposes, rather than functional <https://core.telegram.org/api/bots/inline#inline-feedback>`_.

    For a nicer way to register this handler, have a look at the
    :meth:`~pyrogram.Client.on_chosen_inline_result` decorator.

    Parameters
    ----------
        callback (``Callable``):
            Pass a function that will be called when a new chosen inline result arrives.
            It takes *(client, chosen_inline_result)* as positional arguments (look at the section below for a
            detailed description).

        filters (:obj:`Filter`):
            Pass one or more filters to allow only a subset of chosen inline results to be passed
            in your callback function.

    Other Parameters
    ----------------
        client (:obj:`~pyrogram.Client`):
            The Client itself, useful when you want to call other API methods inside the choose inline result
            handler.

        chosen_inline_result (:obj:`~pyrogram.types.ChosenInlineResult`):
            The received chosen inline result.

    """

    def __init__(self, callback: CallbackFunc, filters: Filter = None) -> None:
        super().__init__(callback, filters)
