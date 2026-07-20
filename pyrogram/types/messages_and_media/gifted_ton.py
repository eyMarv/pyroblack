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

import random

from pyrogram import raw, types
from pyrogram.types.object import Object


class GiftedTon(Object):
    """Toncoins were gifted to a user.

    Parameters
    ----------
        gifter (:obj:`~pyrogram.types.User`, *optional*):
            User that gifted Telegram Premium.
            None if the gift was anonymous.

        receiver (:obj:`~pyrogram.types.User`):
            User that received Telegram Premium.

        ton_amount (``int``):
            The received amount of Toncoins, in the smallest units of the cryptocurrency.

        transaction_id (``str``, *optional*):
            Identifier of the transaction for Telegram Stars purchase.
            For receiver only.

        sticker (:obj:`~pyrogram.types.Sticker`):
            A sticker to be shown in the message.

    """

    def __init__(
        self,
        *,
        gifter: types.User | None = None,
        receiver: types.User,
        ton_amount: int | None = None,
        transaction_id: str | None = None,
        sticker: types.Sticker | None = None,
    ) -> None:
        super().__init__()

        self.gifter = gifter
        self.receiver = receiver
        self.ton_amount = ton_amount
        self.transaction_id = transaction_id
        self.sticker = sticker

    @staticmethod
    async def _parse(
        client,
        action: raw.types.MessageActionGiftTon,
        gifter: raw.base.User | None = None,
        receiver: raw.base.User | None = None,
    ) -> GiftedTon:
        raw_stickers = await client.invoke(
            raw.functions.messages.GetStickerSet(
                stickerset=raw.types.InputStickerSetTonGifts(),
                hash=0,
            ),
        )

        return GiftedTon(
            gifter=types.User._parse(client, gifter),
            receiver=types.User._parse(client, receiver),
            ton_amount=action.crypto_amount,
            transaction_id=action.transaction_id,
            sticker=random.choice(
                types.List(
                    [
                        await types.Sticker._parse(
                            client,
                            doc,
                            {type(i): i for i in doc.attributes},
                        )
                        for doc in raw_stickers.documents
                    ],
                ),
            ),
        )
