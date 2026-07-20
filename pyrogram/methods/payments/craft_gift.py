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
from pyrogram import raw, types, utils


class CraftGift:
    async def craft_gift(
        self: "pyrogram.Client",
        owned_gift_ids: list[str],
    ) -> "types.CraftGiftResult":
        """Crafts a new gift from other gifts that will be permanently lost.

        .. include:: /_includes/usable-by/users.rst

        Parameters
        ----------
            owned_gift_ids (List of ``str``):
                Identifier of the gifts to use for crafting.

        Returns
        -------
            :obj:`~pyrogram.types.CraftGiftResult`: On success, returns the result of gift crafting.

        """
        r = await self.invoke(
            raw.functions.payments.CraftStarGift(
                stargift=[
                    await utils.get_input_stargift(self, owned_gift_id)
                    for owned_gift_id in owned_gift_ids
                ],
            ),
        )

        users = {i.id: i for i in r.users}
        chats = {i.id: i for i in r.chats}

        for u in r.updates:
            if isinstance(u, raw.types.UpdateStarGiftCraftFail):
                return types.CraftGiftResultFail()

            if isinstance(u, raw.types.UpdateNewMessage):
                message = await types.Message._parse(
                    self,
                    u.message,
                    users,
                    chats,
                    business_connection_id=getattr(u, "connection_id", None),
                    raw_reply_to_message=getattr(u, "reply_to_message", None),
                )

                return types.CraftGiftResultSuccess(
                    gift=message.gift,
                )
        return None
