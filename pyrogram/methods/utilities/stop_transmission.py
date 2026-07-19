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

from typing import NoReturn

import pyrogram


class StopTransmission:
    def stop_transmission(self) -> NoReturn:
        """Stop downloading or uploading a file.

        This method must be called inside a progress callback function in order to stop the transmission at the
        desired time. The progress callback is called every time a file chunk is uploaded/downloaded.

        Example:
            .. code-block:: python

                # Stop transmission once the upload progress reaches 50%
                async def progress(current, total, client):
                    if (current * 100 / total) > 50:
                        client.stop_transmission()

                async with app:
                    await app.send_document(
                        "me", "file.zip",
                        progress=progress,
                        progress_args=(app,))

        """
        raise pyrogram.StopTransmission
