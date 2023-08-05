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


class File(Object):
    """Attributes:
        ID: ``0x096a18d5``

    Args:
        type: Either :obj:`storage.FileUnknown <DevLGram.api.types.storage.FileUnknown>`, :obj:`storage.FilePartial <DevLGram.api.types.storage.FilePartial>`, :obj:`storage.FileJpeg <DevLGram.api.types.storage.FileJpeg>`, :obj:`storage.FileGif <DevLGram.api.types.storage.FileGif>`, :obj:`storage.FilePng <DevLGram.api.types.storage.FilePng>`, :obj:`storage.FilePdf <DevLGram.api.types.storage.FilePdf>`, :obj:`storage.FileMp3 <DevLGram.api.types.storage.FileMp3>`, :obj:`storage.FileMov <DevLGram.api.types.storage.FileMov>`, :obj:`storage.FileMp4 <DevLGram.api.types.storage.FileMp4>` or :obj:`storage.FileWebp <DevLGram.api.types.storage.FileWebp>`
        mtime: ``int`` ``32-bit``
        bytes: ``bytes``

    See Also:
        This object can be returned by :obj:`upload.GetFile <DevLGram.api.functions.upload.GetFile>`.
    """

    __slots__ = ["type", "mtime", "bytes"]

    ID = 0x096a18d5
    QUALNAME = "upload.File"

    def __init__(self, *, type, mtime: int, bytes: bytes):
        self.type = type  # storage.FileType
        self.mtime = mtime  # int
        self.bytes = bytes  # bytes

    @staticmethod
    def read(b: BytesIO, *args) -> "File":
        # No flags
        
        type = Object.read(b)
        
        mtime = Int.read(b)
        
        bytes = Bytes.read(b)
        
        return File(type=type, mtime=mtime, bytes=bytes)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(self.type.write())
        
        b.write(Int(self.mtime))
        
        b.write(Bytes(self.bytes))
        
        return b.getvalue()
