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

from .ask import Ask
from .get_listener_matching_with_data import GetListenerMatchingWithData
from .get_listener_matching_with_identifier_pattern import (
    GetListenerMatchingWithIdentifierPattern,
)
from .get_many_listeners_matching_with_data import GetManyListenersMatchingWithData
from .get_many_listeners_matching_with_identifier_pattern import (
    GetManyListenersMatchingWithIdentifierPattern,
)
from .listen import Listen
from .register_next_step_handler import RegisterNextStepHandler
from .remove_listerner import RemoveListener
from .stop_listener import StopListener
from .stop_listening import StopListening
from .wait_for_callback_query import WaitForCallbackQuery
from .wait_for_message import WaitForMessage


class Pyromod(
    Ask,
    GetListenerMatchingWithData,
    GetListenerMatchingWithIdentifierPattern,
    GetManyListenersMatchingWithData,
    GetManyListenersMatchingWithIdentifierPattern,
    Listen,
    RegisterNextStepHandler,
    RemoveListener,
    StopListener,
    StopListening,
    WaitForCallbackQuery,
    WaitForMessage,
):
    pass
