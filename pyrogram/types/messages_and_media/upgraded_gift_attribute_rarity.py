from typing import Optional

from pyrogram import raw

from ..object import Object


class UpgradedGiftAttributeRarity(Object):
    """Describes rarity of an upgraded gift attribute."""

    def __init__(self):
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
    def __init__(self, *, per_mille: int):
        super().__init__()

        self.per_mille = per_mille


class UpgradedGiftAttributeRarityUncommon(UpgradedGiftAttributeRarity):
    pass


class UpgradedGiftAttributeRarityRare(UpgradedGiftAttributeRarity):
    pass


class UpgradedGiftAttributeRarityEpic(UpgradedGiftAttributeRarity):
    pass


class UpgradedGiftAttributeRarityLegendary(UpgradedGiftAttributeRarity):
    pass
