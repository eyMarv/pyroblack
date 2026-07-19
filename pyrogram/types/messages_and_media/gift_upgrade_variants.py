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


import pyrogram
from pyrogram import raw, types
from pyrogram.types.object import Object


class GiftUpgradeVariants(Object):
    """Contains all possible variants of upgraded gifts for the given regular gift.

    Parameters
    ----------
        models (List of :obj:`~pyrogram.types.GiftAttribute`):
            Models that can be chosen for the gift after upgrade.

        symbols (List of :obj:`~pyrogram.types.GiftAttribute`):
            Symbols that can be chosen for the gift after upgrade.

        backdrops (List of :obj:`~pyrogram.types.GiftAttribute`):
            Backdrops that can be chosen for the gift after upgrade.

    """

    def __init__(
        self,
        *,
        models: list["types.GiftAttribute"],
        symbols: list["types.GiftAttribute"],
        backdrops: list["types.GiftAttribute"],
    ) -> None:
        super().__init__()

        self.models = models
        self.symbols = symbols
        self.backdrops = backdrops

    @staticmethod
    async def _parse(
        client: "pyrogram.Client",
        gift_upgrade_attributes: "raw.types.payments.StarGiftUpgradeAttributes",
    ):
        models = types.List()
        symbols = types.List()
        backdrops = types.List()

        for attr in gift_upgrade_attributes.attributes:
            if isinstance(attr, raw.types.StarGiftAttributeModel):
                models.append(await types.GiftAttribute._parse(client, attr, {}, {}))
            elif isinstance(attr, raw.types.StarGiftAttributePattern):
                symbols.append(await types.GiftAttribute._parse(client, attr, {}, {}))
            elif isinstance(attr, raw.types.StarGiftAttributeBackdrop):
                backdrops.append(await types.GiftAttribute._parse(client, attr, {}, {}))

        return GiftUpgradeVariants(
            models=models,
            symbols=symbols,
            backdrops=backdrops,
        )
