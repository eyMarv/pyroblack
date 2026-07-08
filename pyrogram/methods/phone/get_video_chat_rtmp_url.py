#  pyroblack - Telegram MTProto API Client Library for Python
#  Copyright (C) 2022-present Mayuri-Chan <https://github.com/Mayuri-Chan>
#  Copyright (C) 2024-present eyMarv <https://github.com/eyMarv>
#
#  This file is part of pyroblack.
#
#  pyroblack is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Lesser General Public License as published
#  by the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  pyroblack is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public License
#  along with pyroblack.  If not, see <http://www.gnu.org/licenses/>.

from typing import Union

import pyrogram
from pyrogram import types, raw


class GetVideoChatRtmpUrl:
    async def get_video_chat_rtmp_url(
        self: "pyrogram.Client",
        chat_id: Union[int, str],
        replace: bool = False
    ) -> "types.RtmpUrl":
        """Returns RTMP URL for streaming to the chat; requires owner privileges.

        .. include:: /_includes/usable-by/users.rst

        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target chat.
                A chat can be either a basic group, supergroup or a channel.

            replace (``bool``, *optional*):
                Whether to replace the previous stream key or simply return the existing one.
                Defaults to False, i.e., return the existing one.

        Returns:
            :obj:`~pyrogram.types.RtmpUrl`: On success, the RTMP URL and stream key is returned.

        Example:
            .. code-block:: python

                await app.get_video_chat_rtmp_url(chat_id)

        """
        peer = await self.resolve_peer(chat_id)

        if not isinstance(peer, (raw.types.InputPeerChat, raw.types.InputPeerChannel)):
            raise ValueError("Target chat should be group, supergroup or channel.")

        r = await self.invoke(
            raw.functions.phone.GetGroupCallStreamRtmpUrl(
                peer=peer,
                revoke=replace
            )
        )

        return types.RtmpUrl._parse(r)
