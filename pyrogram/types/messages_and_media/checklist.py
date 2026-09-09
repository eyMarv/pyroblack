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
from pyrogram.types.object import Object

from .message import Str


class Checklist(Object):
    """Describes a checklist.

    Parameters
    ----------
        title (``str``):
            Title of the checklist.

        title_entities (List of :obj:`~pyrogram.types.MessageEntity`, *optional*):
            Special entities that appear in the checklist title.
            May contain only Bold, Italic, Underline, Strikethrough, Spoiler, and CustomEmoji entities.

        tasks (List of :obj:`~pyrogram.types.ChecklistTask`, *optional*):
            List of tasks in the checklist.

        others_can_add_tasks (``bool``, *optional*):
            True, if users other than the creator of the list can add tasks to the list.

        others_can_mark_tasks_as_done (``bool``, *optional*):
            True, if users other than the creator of the list can mark tasks as done or not done.

    """

    def __init__(
        self,
        *,
        title: str,
        title_entities: list[types.MessageEntity] | None = None,
        tasks: list[types.ChecklistTask] | None = None,
        others_can_add_tasks: bool | None = None,
        others_can_mark_tasks_as_done: bool | None = None,
        # pyroblack <= 2.7.6 keyword names, accepted so the old constructor
        # call still binds. See the property aliases below.
        entities: list[types.MessageEntity] | None = None,
        can_add_tasks: bool | None = None,
        can_mark_tasks_as_done: bool | None = None,
    ) -> None:
        super().__init__()

        self.title = title
        self.title_entities = title_entities if title_entities is not None else entities
        self.tasks = tasks
        self.others_can_add_tasks = (
            others_can_add_tasks if others_can_add_tasks is not None else can_add_tasks
        )
        self.others_can_mark_tasks_as_done = (
            others_can_mark_tasks_as_done
            if others_can_mark_tasks_as_done is not None
            else can_mark_tasks_as_done
        )

    # pyroblack <= 2.7.6 names. ``entities`` was renamed to ``title_entities``;
    # ``can_add_tasks``/``can_mark_tasks_as_done`` described *your own* rights
    # and were never populated by the parser (the raw ``can_append`` /
    # ``can_complete`` reads were commented out there too), so they mirror the
    # ``others_*`` flags rather than inventing a value.
    @property
    def entities(self) -> list[types.MessageEntity] | None:
        """Deprecated alias of :attr:`title_entities`."""
        return self.title_entities

    @property
    def can_add_tasks(self) -> bool | None:
        """Deprecated alias of :attr:`others_can_add_tasks`."""
        return self.others_can_add_tasks

    @property
    def can_mark_tasks_as_done(self) -> bool | None:
        """Deprecated alias of :attr:`others_can_mark_tasks_as_done`."""
        return self.others_can_mark_tasks_as_done

    @staticmethod
    def _parse(
        client: pyrogram.Client,
        checklist: raw.types.MessageMediaToDo,
        users: dict[int, raw.base.User],
        chats: dict[int, raw.base.User],
    ) -> Checklist:
        completions = {i.id: i for i in getattr(checklist, "completions", [])}

        checklist_tasks = []

        for task in checklist.todo.list:
            checklist_tasks.append(
                types.ChecklistTask._parse(
                    client,
                    task,
                    completions.get(task.id),
                    users,
                    chats,
                ),
            )

        title_entities = [
            types.MessageEntity._parse(client, entity, users)
            for entity in checklist.todo.title.entities
        ]
        title_entities = types.List(filter(lambda x: x is not None, title_entities))
        title = Str(checklist.todo.title.text).init(title_entities) or None

        return Checklist(
            title=title,
            title_entities=title_entities,
            tasks=checklist_tasks,
            others_can_add_tasks=checklist.todo.others_can_append,
            others_can_mark_tasks_as_done=checklist.todo.others_can_complete,
        )
