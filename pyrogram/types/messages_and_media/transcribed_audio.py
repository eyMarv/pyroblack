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

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pyrogram import raw


class TranscribedAudio:
    """Transcribes the audio of a voice message.

    Parameters
    ----------
        transcription_id (``int``):
            Unique identifier of the transcription.

        text (``str``):
            Transcribed text.

        pending (``bool``, *optional*):
            Whether the transcription is pending.

        trial_remains_num (``int``, *optional*):
            Number of trials remaining.

        trial_remains_until_date (``int``, *optional*):
            Date the trial remains until.

    """

    def __init__(
        self,
        *,
        transcription_id: int,
        text: str,
        pending: bool | None = None,
        trial_remains_num: int | None = None,
        trial_remains_until_date: int | None = None,
    ) -> None:
        self.transcription_id = transcription_id
        self.text = text
        self.pending = pending
        self.trial_remains_num = trial_remains_num
        self.trial_remains_until_date = trial_remains_until_date

    @staticmethod
    def _parse(
        transcribe_result: raw.types.messages.TranscribedAudio,
    ) -> TranscribeAudio:
        return TranscribedAudio(
            transcription_id=transcribe_result.id,
            text=transcribe_result.text,
            pending=transcribe_result.pending,
            trial_remains_num=transcribe_result.trial_remains_num,
            trial_remains_until_date=transcribe_result.trial_remains_until_date,
        )
