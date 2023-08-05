# DevLGram - Telegram MTProto API Client Library for Python
# Copyright (C) 2017-2019 Dan Tès <https://github.com/devladityanugraha>
#
# This file is part of DevLGram.
#
# DevLGram is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# DevLGram is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with DevLGram.  If not, see <http://www.gnu.org/licenses/>.

from io import BytesIO

from DevLGram.api.core import *


class UploadWallPaper(Object):
    """Attributes:
        ID: ``0xdd853661``

    Args:
        file: Either :obj:`InputFile <DevLGram.api.types.InputFile>` or :obj:`InputFileBig <DevLGram.api.types.InputFileBig>`
        mime_type: ``str``
        settings: :obj:`WallPaperSettings <DevLGram.api.types.WallPaperSettings>`

    Raises:
        :obj:`RPCError <DevLGram.RPCError>`

    Returns:
        :obj:`WallPaper <DevLGram.api.types.WallPaper>`
    """

    __slots__ = ["file", "mime_type", "settings"]

    ID = 0xdd853661
    QUALNAME = "account.UploadWallPaper"

    def __init__(self, *, file, mime_type: str, settings):
        self.file = file  # InputFile
        self.mime_type = mime_type  # string
        self.settings = settings  # WallPaperSettings

    @staticmethod
    def read(b: BytesIO, *args) -> "UploadWallPaper":
        # No flags
        
        file = Object.read(b)
        
        mime_type = String.read(b)
        
        settings = Object.read(b)
        
        return UploadWallPaper(file=file, mime_type=mime_type, settings=settings)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(self.file.write())
        
        b.write(String(self.mime_type))
        
        b.write(self.settings.write())
        
        return b.getvalue()
