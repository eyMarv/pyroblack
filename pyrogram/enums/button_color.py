#  pyroblack - Telegram MTProto API Client Library for Python
#  Copyright (C) 2017-present Dan <https://github.com/delivrance>
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

from enum import Enum


class ButtonColor(str, Enum):
    """Enumeration of button color styles for inline and reply keyboard buttons.

    These styles control the visual appearance (color) of a button as rendered
    by Telegram clients. Introduced in Bot API 9.4.

    The ``ButtonColor`` values are passed as the ``color`` parameter of
    :obj:`~pyrogram.types.InlineKeyboardButton` and
    :obj:`~pyrogram.types.KeyboardButton`.

    Example:
        .. code-block:: python

            from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
            from pyrogram.enums import ButtonColor

            markup = InlineKeyboardMarkup([[
                InlineKeyboardButton(
                    "Delete",
                    callback_data="delete",
                    color=ButtonColor.DANGER,
                ),
                InlineKeyboardButton(
                    "Confirm",
                    callback_data="confirm",
                    color=ButtonColor.SUCCESS,
                ),
            ]])
    """

    DANGER = "danger"
    """Red button – typically used for destructive or irreversible actions."""

    SUCCESS = "success"
    """Green button – typically used for confirming or positive actions."""

    PRIMARY = "primary"
    """Blue button – typically used for the main / highlighted action."""
