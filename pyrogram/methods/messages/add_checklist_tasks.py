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
from pyrogram import raw, types


class AddChecklistTasks:
    async def add_checklist_tasks(
        self: pyrogram.Client,
        chat_id: int | str,
        message_id: int,
        tasks: list[types.InputChecklistTask],
    ) -> int:
        """Add tasks to a checklist in a message.

        .. include:: /_includes/usable-by/users.rst

        Parameters
        ----------
            chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target chat.
                For your personal cloud (Saved Messages) you can simply use "me" or "self".
                For a contact that exists in your Telegram address book you can use his phone number (str).

            message_id (``int``):
                Identifier of the message containing the checklist.

            tasks (List of :obj:`~pyrogram.types.InputChecklistTask`):
                List of tasks to add to the checklist.

        Returns
        -------
            ``bool``: On success, True is returned.

        Example:
            .. code-block:: python

                await app.add_checklist_tasks(
                    chat_id,
                    message_id,
                    tasks=[
                        types.InputChecklistTask(
                            id=2,
                            text="Task 2"
                        )
                    ]
                )

        """
        await self.invoke(
            raw.functions.messages.AppendTodoList(
                peer=await self.resolve_peer(chat_id),
                msg_id=message_id,
                list=[await task.write(self) for task in tasks],
            ),
        )

        return True
