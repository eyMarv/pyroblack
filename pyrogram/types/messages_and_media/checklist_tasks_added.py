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

from typing import Dict

import pyrogram
from pyrogram import raw, types

from ..object import Object


class ChecklistTasksAdded(Object):
    """Describes a service message about tasks added to a checklist.

    Parameters:
        checklist_message_id (``int``):
            Identifier of the message with the checklist.
            Can be None if the message was deleted.

        tasks (List of :obj:`~pyrogram.types.ChecklistTask`):
            List of tasks added to the checklist.

    """

    def __init__(
        self,
        *,
        checklist_message_id: int,
        tasks: list["types.ChecklistTask"]
    ):

        super().__init__()

        self.checklist_message_id = checklist_message_id
        self.tasks = tasks

    @staticmethod
    def _parse(
        client: "pyrogram.Client",
        message: "raw.types.MessageService",
        users: Dict[int, "raw.base.User"],
        chats: Dict[int, "raw.base.Chat"],
    ) -> "ChecklistTasksAdded":
        action: "raw.types.MessageActionTodoAppendTasks" = message.action

        return ChecklistTasksAdded(
            checklist_message_id=getattr(message.reply_to, "reply_to_msg_id", None),
            tasks=types.List([types.ChecklistTask._parse(client, task, None, users, chats) for task in action.list])
        )
