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

from pyrogram import raw, types
from pyrogram.types.object import Object


class PollOptionAdded(Object):
    """This object represents a service message about an option added to a poll.

    Parameters
    ----------
        poll_message (:obj:`~pyrogram.types.Message`, *optional*):
            Message containing the poll to which the option was added, if known.

        option_persistent_id (``str``):
            Unique identifier of the added option.

        option_text (:obj:`~pyrogram.types.FormattedText`):
            Option text.

    """

    def __init__(
        self,
        *,
        option_persistent_id: str,
        poll_message: "types.Message" = None,
        option_text: "types.FormattedText" = None,
    ) -> None:
        super().__init__()

        self.option_persistent_id = option_persistent_id
        self.poll_message = poll_message
        self.option_text = option_text

    @staticmethod
    def _parse(
        client,
        message: "raw.types.MessageService",
    ) -> "PollOptionAdded":
        action: raw.types.MessageActionPollAppendAnswer = message.action
        answer: raw.types.PollAnswer = action.answer
        return PollOptionAdded(
            option_persistent_id=answer.option.decode("UTF-8"),
            poll_message=None,
            option_text=types.FormattedText._parse(client, answer.text),
        )
