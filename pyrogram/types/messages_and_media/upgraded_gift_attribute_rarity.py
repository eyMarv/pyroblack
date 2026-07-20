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

from typing import Optional

from pyrogram import raw
from pyrogram.types.object import Object


class UpgradedGiftAttributeRarity(Object):
    """Describes rarity of an upgraded gift attribute.

    It can be one of:
    - :obj:`~pyrogram.types.UpgradedGiftAttributeRarityPerMille`
    - :obj:`~pyrogram.types.UpgradedGiftAttributeRarityUncommon`
    - :obj:`~pyrogram.types.UpgradedGiftAttributeRarityRare`
    - :obj:`~pyrogram.types.UpgradedGiftAttributeRarityEpic`
    - :obj:`~pyrogram.types.UpgradedGiftAttributeRarityLegendary`
    """

    def __init__(self) -> None:
        super().__init__()

    @staticmethod
    def _parse(
        rarity: "raw.base.StarGiftAttributeRarity",
    ) -> Optional["UpgradedGiftAttributeRarity"]:
        if isinstance(rarity, raw.types.StarGiftAttributeRarity):
            return UpgradedGiftAttributeRarityPerMille(per_mille=rarity.permille)
        if isinstance(rarity, raw.types.StarGiftAttributeRarityUncommon):
            return UpgradedGiftAttributeRarityUncommon()
        if isinstance(rarity, raw.types.StarGiftAttributeRarityRare):
            return UpgradedGiftAttributeRarityRare()
        if isinstance(rarity, raw.types.StarGiftAttributeRarityEpic):
            return UpgradedGiftAttributeRarityEpic()
        if isinstance(rarity, raw.types.StarGiftAttributeRarityLegendary):
            return UpgradedGiftAttributeRarityLegendary()
        return None


class UpgradedGiftAttributeRarityPerMille(UpgradedGiftAttributeRarity):
    """The rarity is represented as the numeric frequence of the model.

    Parameters
    ----------
        per_mille (``int``):
            The number of upgraded gifts that receive this attribute for each 1000 gifts upgraded.
            If 0, then it can be shown as "<0.1%".

    """

    def __init__(self, *, per_mille: int) -> None:
        super().__init__()

        self.per_mille = per_mille

    @staticmethod
    def _parse(
        rarity: "raw.base.StarGiftAttributeRarity",
    ) -> Optional["UpgradedGiftAttributeRarityPerMille"]:
        if isinstance(rarity, raw.types.StarGiftAttributeRarity):
            return UpgradedGiftAttributeRarityPerMille(per_mille=rarity.permille)
        return None


class UpgradedGiftAttributeRarityUncommon(UpgradedGiftAttributeRarity):
    """The attribute is uncommon."""

    def __init__(self) -> None:
        super().__init__()

    @staticmethod
    def _parse(
        rarity: "raw.base.StarGiftAttributeRarity",
    ) -> Optional["UpgradedGiftAttributeRarityUncommon"]:
        if isinstance(rarity, raw.types.StarGiftAttributeRarityUncommon):
            return UpgradedGiftAttributeRarityUncommon()
        return None


class UpgradedGiftAttributeRarityRare(UpgradedGiftAttributeRarity):
    """The attribute is rare."""

    def __init__(self) -> None:
        super().__init__()

    @staticmethod
    def _parse(
        rarity: "raw.base.StarGiftAttributeRarity",
    ) -> Optional["UpgradedGiftAttributeRarityRare"]:
        if isinstance(rarity, raw.types.StarGiftAttributeRarityRare):
            return UpgradedGiftAttributeRarityRare()
        return None


class UpgradedGiftAttributeRarityEpic(UpgradedGiftAttributeRarity):
    """The attribute is epic."""

    def __init__(self) -> None:
        super().__init__()

    @staticmethod
    def _parse(
        rarity: "raw.base.StarGiftAttributeRarity",
    ) -> Optional["UpgradedGiftAttributeRarityEpic"]:
        if isinstance(rarity, raw.types.StarGiftAttributeRarityEpic):
            return UpgradedGiftAttributeRarityEpic()
        return None


class UpgradedGiftAttributeRarityLegendary(UpgradedGiftAttributeRarity):
    """The attribute is legendary."""

    def __init__(self) -> None:
        super().__init__()

    @staticmethod
    def _parse(
        rarity: "raw.base.StarGiftAttributeRarity",
    ) -> Optional["UpgradedGiftAttributeRarityLegendary"]:
        if isinstance(rarity, raw.types.StarGiftAttributeRarityLegendary):
            return UpgradedGiftAttributeRarityLegendary()
        return None
