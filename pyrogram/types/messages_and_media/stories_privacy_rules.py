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

from pyrogram import enums, raw
from pyrogram.types.object import Object


class StoriesPrivacyRules(Object):
    """A story privacy.

    Parameters
    ----------
        type (:obj:`~pyrogram.enums.StoriesPrivacyRules`):
            Story privacy type.

    """

    def __init__(self, *, type: "enums.StoriesPrivacyRules") -> None:
        super().__init__()
        self.type = type

    def write(self):
        if self.type == enums.StoriesPrivacyRules.PUBLIC:
            return raw.types.InputPrivacyValueAllowAll().write()
        if self.type == enums.StoriesPrivacyRules.CLOSE_FRIENDS:
            return raw.types.InputPrivacyValueAllowCloseFriends().write()
        if self.type == enums.StoriesPrivacyRules.CONTACTS:
            return raw.types.InputPrivacyValueAllowContacts().write()
        if self.type == enums.StoriesPrivacyRules.NO_CONTACTS:
            return raw.types.InputPrivacyValueDisallowContacts().write()
        if self.type == enums.StoriesPrivacyRules.PRIVATE:
            return raw.types.InputPrivacyValueDisallowAll().write()
        return None
