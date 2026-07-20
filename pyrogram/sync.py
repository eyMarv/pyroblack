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

import asyncio
import functools
import inspect
import threading

from pyrogram import types, utils
from pyrogram.methods import Methods
from pyrogram.methods.utilities import compose as compose_module
from pyrogram.methods.utilities import idle as idle_module


def async_to_sync(obj, name) -> None:
    function = getattr(obj, name)
    main_loop = utils.get_event_loop()

    def async_to_sync_gen(agen, loop, is_main_thread):
        async def anext(agen):
            try:
                return await agen.__anext__(), False
            except StopAsyncIteration:
                return None, True

        while True:
            if is_main_thread:
                item, done = loop.run_until_complete(anext(agen))
            else:
                item, done = asyncio.run_coroutine_threadsafe(
                    anext(agen), loop
                ).result()

            if done:
                break

            yield item

    @functools.wraps(function)
    def async_to_sync_wrap(*args, **kwargs):
        coroutine = function(*args, **kwargs)
        loop = utils.get_event_loop()

        if (
            threading.current_thread() is threading.main_thread()
            or not main_loop.is_running()
        ):
            if loop.is_running():
                return coroutine
            if inspect.iscoroutine(coroutine):
                return loop.run_until_complete(coroutine)

            if inspect.isasyncgen(coroutine):
                return async_to_sync_gen(coroutine, loop, True)
        else:
            if inspect.iscoroutine(coroutine):
                if loop.is_running():

                    async def coro_wrapper():
                        return await asyncio.wrap_future(
                            asyncio.run_coroutine_threadsafe(coroutine, main_loop)
                        )

                    return coro_wrapper()
                return asyncio.run_coroutine_threadsafe(coroutine, main_loop).result()

            if inspect.isasyncgen(coroutine):
                if loop.is_running():
                    return coroutine
                return async_to_sync_gen(coroutine, main_loop, False)
        return None

    setattr(obj, name, async_to_sync_wrap)


def wrap(source) -> None:
    for name in dir(source):
        method = getattr(source, name)

        if not name.startswith("_"):
            if inspect.iscoroutinefunction(method) or inspect.isasyncgenfunction(
                method
            ):
                async_to_sync(source, name)


# Wrap all Client's relevant methods
wrap(Methods)

# Wrap types' bound methods
for class_name in dir(types):
    cls = getattr(types, class_name)

    if inspect.isclass(cls):
        wrap(cls)

# Special case for idle and compose, because they are not inside Methods
async_to_sync(idle_module, "idle")
idle = idle_module.idle

async_to_sync(compose_module, "compose")
compose = compose_module.compose
