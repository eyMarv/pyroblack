#  Pyrogram - Telegram MTProto API Client Library for Python
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
from pyrogram.utils import run_sync

log = getLogger(__name__)

PART_SIZE = 512 * 1024          # 512 KB — Telegram's hard limit per part
READ_BUFFER = 4 * 1024 * 1024   # 4 MB read buffer for fast disk I/O
WORKERS_PER_SESSION = 4         # Concurrent in-flight RPCs per TCP session


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

            n_sessions = self.max_download_workers
            dc_id = await self.storage.dc_id()
            pool = await self._get_media_session_pool(dc_id, n_sessions)

            # n_workers is the TOTAL number of parallel uploaders across all sessions
            n_workers = n_sessions * WORKERS_PER_SESSION
            queue = asyncio.Queue(n_workers)

            async def worker(session):
                while True:
                    data = await queue.get()
                    try:
                        if data is None:
                            return

                        for attempt in range(5):
                            try:
                                await session.invoke(data)
                                break
                            except StopTransmission:
                                raise
                            except Exception as e:
                                if attempt == 4:
                                    log.error(f"Upload part failed after 5 attempts: {e}")
                                    # Evict dead session from pool
                                    lock = self._media_sessions_locks.setdefault(
                                        dc_id, asyncio.Lock()
                                    )
                                    async with lock:
                                        sess_list = self.media_sessions.get(dc_id, [])
                                        if session in sess_list:
                                            sess_list.remove(session)
                                    raise
                                log.warning(
                                    f"Retrying upload part (attempt {attempt + 1}): {e}"
                                )
                                await asyncio.sleep(2 ** attempt)
                    finally:
                        queue.task_done()

            def create_rpc(chunk, part_idx, is_big, fid, total_parts):
                if is_big:
                    return raw.functions.upload.SaveBigFilePart(
                        file_id=fid,
                        file_part=part_idx,
                        file_total_parts=total_parts,
                        bytes=chunk,
                    )
                return raw.functions.upload.SaveFilePart(
                    file_id=fid,
                    file_part=part_idx,
                    bytes=chunk,
                )

            # Workers are spawned AFTER file validation succeeds
            worker_tasks: list = []
            fp = None
            next_chunk_task = None
            parts_sent = file_part

            try:
                # Open the file (raises FileNotFoundError, PermissionError, etc.)
                if isinstance(path, (str, PurePath)):
                    fp = open(path, "rb", buffering=READ_BUFFER)
                else:
                    fp = path

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

                file_total_parts = ceil(file_size / PART_SIZE)
                is_big = file_size > 10 * 1024 * 1024
                is_missing_part = file_id is not None
                file_id = file_id or self.rnd_id()
                md5_sum = md5() if not is_big and not is_missing_part else None

                # Validation passed — spawn workers (round-robin across sessions)
                worker_tasks = [
                    self.loop.create_task(worker(pool[i % n_sessions]))
                    for i in range(n_workers)
                ]

                fp.seek(PART_SIZE * file_part)
                parts_sent = file_part
                # Prime the first read before entering the loop (prefetch overlap)
                next_chunk_task = self.loop.create_task(run_sync(fp.read, PART_SIZE))

                while True:
                    chunk = await next_chunk_task
                    # Start reading the NEXT chunk while we process this one
                    next_chunk_task = self.loop.create_task(
                        run_sync(fp.read, PART_SIZE)
                    )

                    if not chunk:
                        next_chunk_task.cancel()
                        if not is_big and not is_missing_part:
                            md5_sum = md5_sum.hexdigest()  # type: ignore
                        break

                    # Liveness check: if all workers died, surface the failure
                    if all(t.done() for t in worker_tasks):
                        for t in worker_tasks:
                            exc = t.exception()
                            if exc is not None:
                                raise exc
                        raise RuntimeError("All upload workers exited unexpectedly")

                    await queue.put(
                        create_rpc(
                            chunk, parts_sent, is_big, file_id, file_total_parts
                        )
                    )

                    if is_missing_part:
                        next_chunk_task.cancel()
                        for _ in range(n_workers):
                            await queue.put(None)
                        results = await asyncio.gather(
                            *worker_tasks, return_exceptions=True
                        )
                        for r in results:
                            if isinstance(r, BaseException) and not isinstance(
                                r, asyncio.CancelledError
                            ):
                                raise r
                        return None

                    if not is_big and not is_missing_part:
                        md5_sum.update(chunk)  # type: ignore

                    parts_sent += 1

                    if (
                        progress
                        and parts_sent % max(1, file_total_parts // 10) == 0
                    ):
                        func = partial(
                            progress,
                            min(parts_sent * PART_SIZE, file_size),
                            file_size,
                            *progress_args,
                        )
                        if iscoroutinefunction(progress):
                            await func()
                        else:
                            await self.loop.run_in_executor(self.executor, func)

                # Main loop ended cleanly — drain workers and check for failures
                for _ in range(n_workers):
                    await queue.put(None)
                results = await asyncio.gather(
                    *worker_tasks, return_exceptions=True
                )
                for r in results:
                    if isinstance(r, BaseException) and not isinstance(
                        r, asyncio.CancelledError
                    ):
                        raise r

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

            except StopTransmission:
                raise
            except Exception as e:
                log.error(
                    f"Error during file upload at part {parts_sent}: {e}",
                    exc_info=True,
                )
                raise
            finally:
                # Cancel any straggler worker tasks (also handles validation-failure path
                # where worker_tasks is still []).
                for t in worker_tasks:
                    if not t.done():
                        t.cancel()
                if worker_tasks:
                    await asyncio.gather(*worker_tasks, return_exceptions=True)
                # Cancel pending pre-read
                try:
                    if next_chunk_task is not None and not next_chunk_task.done():
                        next_chunk_task.cancel()
                except Exception:
                    pass
                # Close the file only if WE opened it (don't close caller-supplied BinaryIO)
                if fp is not None and isinstance(path, (str, PurePath)):
                    try:
                        fp.close()
                    except Exception:
                        pass

    async def preload(self, fp, part_size):
        return await run_sync(fp.read, part_size)
