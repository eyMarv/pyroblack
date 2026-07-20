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

import pyrogram
from pyrogram import raw, types
from pyrogram.types.object import Object


class GiveawayCompleted(Object):
    """This object represents a service message about the completion of a giveaway without public winners.

    Parameters
    ----------
        winner_count (``int``):
            Number of winners in the giveaway

        unclaimed_prize_count (``int``, *optional*):
            Number of undistributed prizes

        giveaway_message (:obj:`~pyrogram.types.Message`, *optional*):
            Message with the giveaway that was completed, if it wasn't deleted

        is_star_giveaway (``bool``, *optional*):
            True, if the giveaway is a Telegram Star giveaway. Otherwise, currently, the giveaway is a Telegram Premium giveaway.

    """

    def __init__(
        self,
        *,
        client: pyrogram.Client = None,
        winner_count: int,
        unclaimed_prize_count: int | None = None,
        giveaway_message: types.Message = None,
        is_star_giveaway: bool | None = None,
    ) -> None:
        super().__init__(client)

        self.winner_count = winner_count
        self.unclaimed_prize_count = unclaimed_prize_count
        self.giveaway_message = giveaway_message
        self.is_star_giveaway = is_star_giveaway

    @staticmethod
    def _parse(
        client,
        giveaway_results: raw.types.MessageActionGiveawayResults,
        message_id: int | None = None,
    ) -> GiveawayCompleted:
        if isinstance(giveaway_results, raw.types.MessageActionGiveawayResults):
            return GiveawayCompleted(
                client=client,
                winner_count=giveaway_results.winners_count,
                unclaimed_prize_count=getattr(
                    giveaway_results, "unclaimed_count", None
                ),
                giveaway_message=types.Message(
                    client=client,
                    id=message_id,
                )
                if message_id
                else None,
                is_star_giveaway=getattr(giveaway_results, "stars", None),
            )
        return None
