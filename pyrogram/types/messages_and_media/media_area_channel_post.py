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

from .media_area import MediaArea


class MediaAreaChannelPost(MediaArea):
    """A channel post media area.

    Parameters
    ----------
        coordinates (:obj:`~pyrogram.types.MediaAreaCoordinates`):
            Media area coordinates.

        chat (:obj:`~pyrogram.types.Chat`):
            Information about origin channel.

        message_id (``int``):
            The channel post message id.

    """

    def __init__(
        self,
        coordinates: "types.MediaAreaCoordinates",
        chat: "types.Chat",
        message_id: int,
    ) -> None:
        super().__init__(coordinates=coordinates)

        self.coordinates = coordinates
        self.chat = chat
        self.message_id = message_id

    async def _parse(
        self: "pyrogram.Client",
        media_area: "raw.types.MediaAreaChannelPost",
    ) -> "MediaAreaChannelPost":
        channel_id = utils.get_channel_id(media_area.channel_id)
        chat = types.Chat._parse_chat(
            self,
            (
                await self.invoke(
                    raw.functions.channels.GetChannels(
                        id=[await self.resolve_peer(channel_id)],
                    ),
                )
            ).chats[0],
        )
        return MediaAreaChannelPost(
            coordinates=types.MediaAreaCoordinates._parse(media_area.coordinates),
            chat=chat,
            message_id=media_area.msg_id,
        )
