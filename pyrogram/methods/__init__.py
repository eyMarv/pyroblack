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

from .account import Account
from .advanced import Advanced
from .auth import Auth
from .bots import Bots
from .business import TelegramBusiness
from .chat_topics import ChatTopics
from .chats import Chats
from .contacts import Contacts
from .decorators import Decorators
from .folders import Folders
from .invite_links import InviteLinks
from .messages import Messages
from .password import Password
from .payments import Payments
from .phone import Phone
from .premium import Premium
from .pyromod import Pyromod
from .stickers import Stickers
from .stories import Stories
from .users import Users
from .utilities import Utilities


class Methods(
    Decorators,
    Advanced,
    Auth,
    Account,
    Bots,
    Chats,
    ChatTopics,
    Contacts,
    InviteLinks,
    Messages,
    Password,
    Payments,
    Premium,
    Folders,
    Phone,
    Pyromod,
    Stickers,
    Stories,
    TelegramBusiness,
    Users,
    Utilities,
):
    pass
