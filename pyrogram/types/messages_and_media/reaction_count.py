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

from typing import TYPE_CHECKING, Optional

from pyrogram.types.object import Object

from .reaction_type import ReactionType

if TYPE_CHECKING:
    from pyrogram import raw


class ReactionCount(Object):
    """Represents a reaction added to a message along with the number of times it was added.

    Parameters
    ----------
        type (:obj:`~pyrogram.types.ReactionType`):
            Reaction type.

        total_count (``int``):
            Total reaction count.

        chosen_order (``int``):
            Chosen reaction order.
            Available for chosen reactions.

    """

    def __init__(
        self, *, type: ReactionType, total_count: int, chosen_order: int
    ) -> None:
        super().__init__()
        self.type = type
        self.total_count = total_count
        self.chosen_order = chosen_order

    @staticmethod
    def _parse(
        update: "raw.types.ReactionCount",
    ) -> Optional["ReactionCount"]:
        return ReactionCount(
            type=ReactionType._parse(update.reaction),
            total_count=update.count,
            chosen_order=update.chosen_order,
        )
