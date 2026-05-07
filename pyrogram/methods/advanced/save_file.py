#  Pyrogram - Telegram MTProto API Client Library for Python
#  Copyright (C) 2017-present Dan <https://github.com/delivrance>
#
#  This file is part of Pyrogram.
#
#  Pyrogram is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Lesser General Public License as published
#  by the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  Pyrogram is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public License
#  along with Pyrogram.  If not, see <http://www.gnu.org/licenses/>.

import asyncio
from functools import partial
from inspect import iscoroutinefunction
from logging import getLogger
from math import ceil
from io import SEEK_END
from hashlib import md5
from pathlib import PurePath
from typing import Union, BinaryIO, Callable

import pyrogram
from pyrogram import StopTransmission, raw
from pyrogram.session import Session
from pyrogram.utils import run_sync

log = getLogger(__name__)


class SaveFile:
    async def save_file(
        self: "pyrogram.Client",
        path: Union[str, BinaryIO],
        file_id: int = None,
        file_part: int = 0,
        progress: Callable = None,
        progress_args: tuple = (),
    ):
        """Upload a file onto Telegram servers, without actually sending the message to anyone.
        Useful whenever an InputFile type is required.

        .. note::

            This is a utility method intended to be used **only** when working with raw
            :obj:`functions <pyrogram.api.functions>` (i.e: a Telegram API method you wish to use which is not
            available yet in the Client class as an easy-to-use method).

        .. include:: /_includes/usable-by/users-bots.rst

        Parameters:
            path (``str`` | ``BinaryIO``):
                The path of the file you want to upload that exists on your local machine or a binary file-like object
                with its attribute ".name" set for in-memory uploads.

            file_id (``int``, *optional*):
                In case a file part expired, pass the file_id and the file_part to retry uploading that specific chunk.

            file_part (``int``, *optional*):
                In case a file part expired, pass the file_id and the file_part to retry uploading that specific chunk.

            progress (``Callable``, *optional*):
                Pass a callback function to view the file transmission progress.
                The function must take *(current, total)* as positional arguments (look at Other Parameters below for a
                detailed description) and will be called back each time a new file chunk has been successfully
                transmitted.

            progress_args (``tuple``, *optional*):
                Extra custom arguments for the progress callback function.
                You can pass anything you need to be available in the progress callback scope; for example, a Message
                object or a Client instance in order to edit the message with the updated progress status.

        Other Parameters:
            current (``int``):
                The amount of bytes transmitted so far.

            total (``int``):
                The total size of the file.

            *args (``tuple``, *optional*):
                Extra custom arguments as defined in the ``progress_args`` parameter.
                You can either keep ``*args`` or add every single extra argument in your function signature.

        Returns:
            ``InputFile``: On success, the uploaded file is returned in form of an InputFile object.

        Raises:
            RPCError: In case of a Telegram RPC error.
        """
        async with self.save_file_semaphore:
            if path is None:
                return None

            async def worker(session):
                while True:
                    data = await queue.get()
                    if data is None:
                        return
                    for attempt in range(3):
                        try:
                            await session.invoke(data)
                            break
                        except Exception as e:
                            log.warning(f"Retrying part due to error: {e}")
                            await asyncio.sleep(2 ** attempt)

            def create_rpc(chunk, file_part, is_big, file_id, file_total_parts):
                if is_big:
                    return raw.functions.upload.SaveBigFilePart(
                        file_id=file_id,
                        file_part=file_part,
                        file_total_parts=file_total_parts,
                        bytes=chunk,
                    )
                else:
                    return raw.functions.upload.SaveFilePart(
                        file_id=file_id,
                        file_part=file_part,
                        bytes=chunk
                    )

            part_size = 512 * 1024
            queue = asyncio.Queue(16)

            with (
                open(path, "rb", buffering=4096)
                if isinstance(path, (str, PurePath))
                else path
            ) as fp:
                file_name = getattr(fp, "name", "file.jpg")
                fp.seek(0, SEEK_END)
                file_size = fp.tell()
                fp.seek(0)

                if file_size == 0:
                    raise ValueError("File size equals to 0 B")

                file_size_limit_mib = (
                    4000 if self.me.is_premium else 2000  # type: ignore
                )

                if file_size > file_size_limit_mib * 1024 * 1024:
                    raise ValueError(
                        f"Can't upload files bigger than {file_size_limit_mib} MiB"
                    )

                file_total_parts = ceil(file_size / part_size)
                is_big = file_size > 100 * 1024 * 1024
                pool_size = 2 if is_big else 1
                workers_count = 10 if is_big else 1
                is_missing_part = file_id is not None
                file_id = file_id or self.rnd_id()
                md5_sum = md5() if not is_big and not is_missing_part else None

                pool = [
                    Session(
                        self,
                        await self.storage.dc_id(),
                        await self.storage.auth_key(),
                        await self.storage.test_mode(),
                        is_media=True,
                    )
                    for _ in range(pool_size)
                ]

                workers = [
                    self.loop.create_task(worker(session))
                    for session in pool
                    for _ in range(workers_count)
                ]

                try:
                    for session in pool:
                        await session.start()

                    fp.seek(part_size * file_part)
                    next_chunk_task = self.loop.create_task(self.preload(fp, part_size))

                    while True:
                        chunk = await next_chunk_task
                        next_chunk_task = self.loop.create_task(self.preload(fp, part_size))

                        if not chunk:
                            next_chunk_task.cancel()
                            if not is_big and not is_missing_part:
                                md5_sum = md5_sum.hexdigest()  # type: ignore
                            break

                        await queue.put(
                            create_rpc(chunk, file_part, is_big, file_id, file_total_parts)
                        )

                        if is_missing_part:
                            return

                        if not is_big and not is_missing_part:
                            md5_sum.update(chunk)  # type: ignore

                        file_part += 1

                        if progress and file_total_parts >= 10 and file_part % (file_total_parts // 10) == 0:
                            func = partial(
                                progress,
                                min(file_part * part_size, file_size),
                                file_size,
                                *progress_args,
                            )

                            if iscoroutinefunction(progress):
                                await func()
                            else:
                                await self.loop.run_in_executor(self.executor, func)
                except StopTransmission:
                    raise
                except Exception as e:
                    log.error(f"Error during file upload at part {file_part}: {e}", exc_info=True)
                else:
                    if is_big:
                        return raw.types.InputFileBig(
                            id=file_id,
                            parts=file_total_parts,
                            name=file_name,
                        )
                    else:
                        return raw.types.InputFile(
                            id=file_id,
                            parts=file_total_parts,
                            name=file_name,
                            md5_checksum=md5_sum,  # type: ignore
                        )
                finally:
                    try:
                        if "next_chunk_task" in locals() and next_chunk_task and not next_chunk_task.done():
                            next_chunk_task.cancel()
                    except Exception:
                        pass

                    for _ in workers:
                        await queue.put(None)

                    await asyncio.gather(*workers)

                    for session in pool:
                        await session.stop()

    async def preload(self, fp, part_size):
        return await run_sync(fp.read, part_size)
