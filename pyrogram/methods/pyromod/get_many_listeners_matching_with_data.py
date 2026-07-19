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

from typing import TYPE_CHECKING

from pyrogram.types import Identifier, Listener

if TYPE_CHECKING:
    import pyrogram


class GetManyListenersMatchingWithData:
    def get_many_listeners_matching_with_data(
        self: "pyrogram.Client",
        data: Identifier,
        listener_type: "pyrogram.enums.ListenerTypes",
    ) -> list[Listener]:
        """Gets multiple listener that matches the given data.

        .. include:: /_includes/usable-by/users-bots.rst

        Parameters
        ----------
            data (:obj:`~pyrogram.types.Identifier`):
                The Identifier to match agains.

            listener_type (:obj:`~pyrogram.enums.ListenerTypes`):
                The type of listener to get.

        Returns
        -------
            List of :obj:`~pyrogram.types.Listener`: On success, a list of Listener is returned.

        """
        listeners = []
        for listener in self.listeners[listener_type]:
            if listener.identifier.matches(data):
                listeners.append(listener)
        return listeners
