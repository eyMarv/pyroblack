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

from typing import List, Optional

from pyrogram import enums, types

from ..object import Object


class InputChecklist(Object):
    """Describes a checklist to create.

    Parameters:
        title (``str``):
            Title of the checklist, 1-255 characters.

        tasks (List of :obj:`~pyrogram.types.InputChecklistTask`):
            List of 1-30 tasks in the checklist.

        parse_mode (:obj:`~pyrogram.enums.ParseMode`, *optional*):
            The parse mode to use for the checklist.

        entities (List of :obj:`~pyrogram.types.MessageEntity`, *optional*):
            List of special entities that appear in the checklist title.

        others_can_add_tasks (``bool``, *optional*):
            Pass True if other users can add tasks to the checklist.

        others_can_mark_tasks_as_done (``bool``, *optional*):
            Pass True if other users can mark tasks as done or not done in the checklist.
    """

    def __init__(
        self,
        title: str,
        tasks: List["types.InputChecklistTask"],
        parse_mode: Optional["enums.ParseMode"] = None,
        entities: Optional[List["types.MessageEntity"]] = None,
        others_can_add_tasks: Optional[bool] = None,
        others_can_mark_tasks_as_done: Optional[bool] = None,
    ):
        super().__init__()

        self.title = title
        self.tasks = tasks
        self.parse_mode = parse_mode
        self.entities = entities
        self.others_can_add_tasks = others_can_add_tasks
        self.others_can_mark_tasks_as_done = others_can_mark_tasks_as_done
