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

from ..object import Object

import pyrogram
from pyrogram import raw, types


class PaidReactionType(Object):
    """This object describes the type of paid message reaction.
    
    It can be one of:

    - :obj:`~pyrogram.types.PaidReactionTypeRegular`
    - :obj:`~pyrogram.types.PaidReactionTypeAnonymous`
    - :obj:`~pyrogram.types.PaidReactionTypeChat`

    """

    def __init__(self):
        super().__init__()
    
    async def write(
        self,
        client: "pyrogram.Client",
    ):
        if isinstance(self, PaidReactionTypeChat):
            return self._raw(
                peer=await client.resolve_peer(self.chat_id)
            )
        else:
            return self._raw()



class PaidReactionTypeRegular(PaidReactionType):
    """A paid reaction on behalf of the current user.

    """
    def __init__(self):
        super().__init__()

        self._raw = raw.types.PaidReactionPrivacyDefault


class PaidReactionTypeAnonymous(PaidReactionType):
    """An anonymous paid reaction.
    
    """
    def __init__(self):
        super().__init__()

        self._raw = raw.types.PaidReactionPrivacyAnonymous


class PaidReactionTypeChat(PaidReactionType):
    """A paid reaction on behalf of an owned chat.

    It is intended to be used with :obj:`~pyrogram.Client.`.

    Parameters:
        chat_id (``int``):
            Unique identifier (int) or username (str) of the target chat.
    
    """

    def __init__(self, chat_id: int):
        super().__init__()

        self.chat_id = chat_id
        self._raw = raw.types.PaidReactionPrivacyPeer
