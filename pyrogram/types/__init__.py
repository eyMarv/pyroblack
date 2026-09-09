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

from . import (
    authorization,
    bots_and_keyboards,
    business,
    chat_drafts,
    chat_topics,
    inline_mode,
    input_media,
    input_message_content,
    input_paid_media,
    input_privacy_rule,
    message_origin,
    messages_and_media,
    stories,
    user_and_chats,
)
from .authorization import *
from .bots_and_keyboards import *
from .business import *
from .chat_drafts import *
from .chat_topics import *
from .inline_mode import *
from .input_media import *
from .input_message_content import *
from .input_paid_media import *
from .input_privacy_rule import *
from .list import List
from .message_origin import *
from .messages_and_media import *
from .object import Object
from .pyromod import Identifier, Listener
from .stories import *
from .update import Update
from .user_and_chats import *

# pyroblack <= 2.7.6 published ``__all__`` here, assembled from each
# sub-package. Restored so ``from pyrogram.types import *`` and tooling that
# reads ``pyrogram.types.__all__`` keep working.
__all__ = [
    "Identifier",
    "List",
    "Listener",
    "Object",
    "Update",
]
__all__ += [
    *authorization.__all__,
    *bots_and_keyboards.__all__,
    *business.__all__,
    *chat_drafts.__all__,
    *chat_topics.__all__,
    *inline_mode.__all__,
    *input_media.__all__,
    *input_message_content.__all__,
    *input_paid_media.__all__,
    *input_privacy_rule.__all__,
    *message_origin.__all__,
    *messages_and_media.__all__,
    *stories.__all__,
    *user_and_chats.__all__,
]
# Several names are declared by more than one sub-package (the later star-import
# wins at runtime); keep ``__all__`` free of duplicates. Note that ``list`` is
# shadowed in this namespace by the ``pyrogram.types.list`` submodule, so the
# builtin is reached through ``dict.fromkeys(...).keys()`` instead.
__all__ = [*dict.fromkeys(__all__)]
