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
        pyrogram.types.Update,
        Any,
        Any,
    ],
    Any,
]


class RawUpdateHandler(Handler):
    """The Raw Update handler class. Used to handle raw updates. It is intended to be used with
    :meth:`~pyrogram.Client.add_handler`.

    For a nicer way to register this handler, have a look at the
    :meth:`~pyrogram.Client.on_raw_update` decorator.

    Parameters
    ----------
        callback (``Callable``):
            A function that will be called when a new update is received from the server. It takes
            *(client, update, users, chats)* as positional arguments (look at the section below for
            a detailed description).

        filters (:obj:`Filters`):
            Pass one or more filters to allow only a subset of callback queries to be passed
            in your callback function.

    Other Parameters
    ----------------
        client (:obj:`~pyrogram.Client`):
            The Client itself, useful when you want to call other API methods inside the update handler.

        update (:obj:`~pyrogram.raw.base.Update`):
            The received update, which can be one of the many single Updates listed in the
            :obj:`~pyrogram.raw.base.Update` base type.

        users (``dict``):
            Dictionary of all :obj:`~pyrogram.raw.base.User` mentioned in the update.
            You can access extra info about the user (such as *first_name*, *last_name*, etc...) by using
            the IDs you find in the *update* argument (e.g.: *users[1768841572]*).

        chats (``dict``):
            Dictionary of all :obj:`~pyrogram.raw.base.Chat` and
            :obj:`~pyrogram.raw.types.Channel` mentioned in the update.
            You can access extra info about the chat (such as *title*, *participants_count*, etc...)
            by using the IDs you find in the *update* argument (e.g.: *chats[1701277281]*).

    Note:
        The following Empty or Forbidden types may exist inside the *users* and *chats* dictionaries.
        They mean you have been blocked by the user or banned from the group/channel.

        - :obj:`~pyrogram.raw.types.UserEmpty`
        - :obj:`~pyrogram.raw.types.ChatEmpty`
        - :obj:`~pyrogram.raw.types.ChatForbidden`
        - :obj:`~pyrogram.raw.types.ChannelForbidden`

    """

    def __init__(self, callback: CallbackFunc, filters: Filter = None) -> None:
        super().__init__(callback, filters)
