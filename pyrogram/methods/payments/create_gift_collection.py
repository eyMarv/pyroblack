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
from pyrogram import raw, types, utils


class CreateGiftCollection:
    async def create_gift_collection(
        self: pyrogram.Client,
        owner_id: int | str,
        name: str,
        gift_ids: list[str],
    ) -> types.GiftCollection:
        """Creates a collection from gifts on the current user's or a channel's profile page.

        .. include:: /_includes/usable-by/users.rst

        Parameters
        ----------
            owner_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target chat.
                For your personal cloud (Saved Messages) you can simply use "me" or "self".

            name (``str``):
                Name of the collection, 1-12 characters.

            gift_ids (List of ``str``):
                Identifier of the gifts to add to the collection.

        Returns
        -------
            :obj:`~pyrogram.types.GiftCollection`: On success, a created collection is returned.

        Example:
            .. code-block:: python

                await create_gift_collection("me", "My best gifts!", ["https://t.me/nft/NekoHelmet-9215"])

        """
        r = await self.invoke(
            raw.functions.payments.CreateStarGiftCollection(
                peer=await self.resolve_peer(owner_id),
                title=name,
                stargift=[
                    await utils.get_input_stargift(self, owned_gift_id)
                    for owned_gift_id in gift_ids
                ],
            ),
        )

        return await types.GiftCollection._parse(self, r)
