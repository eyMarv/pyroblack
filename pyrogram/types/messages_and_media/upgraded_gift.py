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

import pyrogram
from pyrogram import raw, types, utils
from ..object import Object


class UpgradedGift(Object):
    """Describes an upgraded gift that can be gifted to another user or transferred to TON blockchain as an NFT.

    Parameters:
        id (``int``):
            Unique identifier of the gift.

        title (``str``):
            The title of the upgraded gift.

        name (``str``):
            Unique name of the upgraded gift.

        number (``int``):
            Unique number of the upgraded gift among gifts upgraded from the same gift.

        total_upgraded_count (``int``):
            Total number of gifts that were upgraded from the same gift.

        max_upgraded_count (``int``):
            The maximum number of gifts that can be upgraded from the same gift.

        owner_id (:obj:`~pyrogram.types.User`, *optional*):
            User identifier of the user or the chat that owns the upgraded gift; may be None if unknown.

        owner_address (``str``, *optional*):
            Address of the gift NFT owner in TON blockchain.

        owner_name (``str``, *optional*):
            Name of the owner for the case when owner identifier and address aren't known.

        gift_address (``str``, *optional*):
            Address of the gift NFT in TON blockchain.

        link (``str``, *property*):
            The link is a link to an upgraded gift.

    """

    def __init__(
        self,
        *,
        client: "pyrogram.Client" = None,
        id: int,
        title: str,
        name: str,
        number: int,
        total_upgraded_count: int,
        max_upgraded_count: int,
        owner_id: Optional["types.Chat"] = None,
        owner_address: Optional[str] = None,
        owner_name: Optional[str] = None,
        gift_address: Optional[str] = None,
        _raw: "raw.types.StarGiftUnique" = None,
    ):
        super().__init__(client)

        self.id = id
        self.title = title
        self.name = name
        self.number = number
        self.total_upgraded_count = total_upgraded_count
        self.max_upgraded_count = max_upgraded_count
        self.owner_id = owner_id
        self.owner_address = owner_address
        self.owner_name = owner_name
        self.gift_address = gift_address
        self._raw = _raw  # TODO


    @staticmethod
    def _parse(
        client,
        star_gift: "raw.types.StarGiftUnique",
        users: dict
    ) -> "UpgradedGift":
        owner_id = utils.get_raw_peer_id(getattr(star_gift, "owner_id", None))
        return UpgradedGift(
            id=star_gift.id,
            title=star_gift.title,
            name=star_gift.slug,
            number=star_gift.num,
            total_upgraded_count=star_gift.availability_issued,
            max_upgraded_count=star_gift.availability_total,
            owner_id=types.Chat._parse_user_chat(
                client,
                users.get(owner_id, owner_id)
            ),
            owner_address=getattr(star_gift, "owner_address", None),
            owner_name=getattr(star_gift, "owner_name", None),
            gift_address=getattr(star_gift, "gift_address", None),
            _raw=star_gift,
            client=client
        )

    @property
    def link(self) -> str:
        return f"https://t.me/nft/{self.name}"
