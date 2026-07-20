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

import logging

import pyrogram
from pyrogram import raw, types

log = logging.getLogger(__name__)


class GetAvailableEffects:
    async def get_available_effects(
        self: "pyrogram.Client",
    ) -> list["types.AvailableEffect"]:
        """Get all available effects.

        .. include:: /_includes/usable-by/users.rst

        Returns:
            List of :obj:`~pyrogram.types.AvailableEffect`: A list of available effects is returned.

        Example:
            .. code-block:: python

                # Get all available effects
                await app.get_available_effects()

        """
        r = await self.invoke(raw.functions.messages.GetAvailableEffects(hash=0))

        documents = {d.id: d for d in r.documents}

        return types.List(
            [
                await types.AvailableEffect._parse(
                    self,
                    effect,
                    documents.get(effect.effect_sticker_id),
                )
                for effect in r.effects
            ],
        )
