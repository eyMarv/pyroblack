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

# Telegram hard limits
# Each part must be a multiple of 1 KB and ≤ 512 KB.
# The total number of parts must not exceed 4000.
PART_SIZE = 512 * 1024          # 512 KB — maximum allowed per part
READ_BUFFER = 4 * 1024 * 1024   # 4 MB read buffer for fast disk I/O


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
            path (``str`` | ``BinaryIO``):\
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

            # ------------------------------------------------------------------
            # Multi-connection parallel upload pipeline (Nekozee technique)
            # ------------------------------------------------------------------
            # Upload bottleneck is identical to download:
            #   1 Session = 1 TCP socket = 1 SaveFilePart in-flight at a time.
            #
            # We reuse the same _get_media_session_pool() used by downloads so
            # sessions stay warm across uploads AND downloads (no reconnect cost).
            # Parts are dispatched round-robin across all N sessions so every
            # TCP connection independently saturates its share of bandwidth.
            # ------------------------------------------------------------------

            n_workers = self.max_download_workers   # reuse same tunable knob
            # Queue depth = 2× worker count so readers stay ahead of senders
            queue_depth = n_workers * 2

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

            # Each worker drains its own dedicated queue (one queue per session)
            # so parts are dispatched in-order per connection.
            worker_queues = [asyncio.Queue(queue_depth) for _ in range(n_workers)]

            async def worker(session, q: asyncio.Queue):
                """Drain one per-session queue, retrying on transient errors."""
                while True:
                    data = await q.get()
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
                                raise
                            log.warning(f"Retrying upload part (attempt {attempt + 1}): {e}")
                            await asyncio.sleep(2 ** attempt)

            with (
                open(path, "rb", buffering=READ_BUFFER)
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

                file_total_parts = ceil(file_size / PART_SIZE)
                # Telegram requires SaveBigFilePart for files > 10 MB
                is_big = file_size > 10 * 1024 * 1024
                is_missing_part = file_id is not None
                file_id = file_id or self.rnd_id()
                md5_sum = md5() if not is_big and not is_missing_part else None

                # Reuse the warm media-session pool (same pool as downloads)
                dc_id = await self.storage.dc_id()
                pool = await self._get_media_session_pool(dc_id, n_workers)

                # Spin up one worker coroutine per session
                worker_tasks = [
                    self.loop.create_task(worker(pool[i], worker_queues[i]))
                    for i in range(n_workers)
                ]

                try:
                    fp.seek(PART_SIZE * file_part)

                    # Pre-read the first chunk in the executor so the loop
                    # starts with data immediately available.
                    next_chunk_task = self.loop.create_task(
                        run_sync(fp.read, PART_SIZE)
                    )

                    parts_sent = file_part

                    while True:
                        chunk = await next_chunk_task

                        # Pre-fetch next chunk while we enqueue this one
                        next_chunk_task = self.loop.create_task(
                            run_sync(fp.read, PART_SIZE)
                        )

                        if not chunk:
                            next_chunk_task.cancel()
                            if not is_big and not is_missing_part:
                                md5_sum = md5_sum.hexdigest()  # type: ignore
                            break

                        rpc = create_rpc(chunk, parts_sent, is_big, file_id, file_total_parts)

                        # Route to the session that owns this part index (round-robin)
                        target_q = worker_queues[parts_sent % n_workers]
                        await target_q.put(rpc)

                        if is_missing_part:
                            # Just re-uploading one expired part — done
                            break

                        if not is_big and not is_missing_part:
                            md5_sum.update(chunk)  # type: ignore

                        parts_sent += 1

                        if progress:
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

                except StopTransmission:
                    raise
                except Exception as e:
                    log.error(
                        f"Error during file upload at part {parts_sent}: {e}",
                        exc_info=True,
                    )
                else:
                    # Wait for all queued parts to finish sending
                    for q in worker_queues:
                        await q.put(None)   # poison pill
                    await asyncio.gather(*worker_tasks, return_exceptions=True)

                    if is_big:
                        return raw.functions.InputFileBig(
                            id=file_id,
                            parts=file_total_parts,
                            name=file_name,
                        )
                    else:
                        return raw.functions.InputFile(
                            id=file_id,
                            parts=file_total_parts,
                            name=file_name,
                            md5_checksum=md5_sum,  # type: ignore
                        )
                finally:
                    # Cancel the pre-read task if still running
                    try:
                        if "next_chunk_task" in locals() and not next_chunk_task.done():
                            next_chunk_task.cancel()
                    except Exception:
                        pass

                    # Drain all queues so workers exit cleanly
                    for q in worker_queues:
                        try:
                            await q.put(None)
                        except Exception:
                            pass

                    await asyncio.gather(*worker_tasks, return_exceptions=True)
                    # Note: sessions are NOT stopped — they belong to the shared pool
