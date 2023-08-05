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


class GetCdnFileHashes(Object):
    """Attributes:
        ID: ``0x4da54231``

    Args:
        file_token: ``bytes``
        offset: ``int`` ``32-bit``

    Raises:
        :obj:`RPCError <DevLGram.RPCError>`

    Returns:
        List of :obj:`FileHash <DevLGram.api.types.FileHash>`
    """

    __slots__ = ["file_token", "offset"]

    ID = 0x4da54231
    QUALNAME = "upload.GetCdnFileHashes"

    def __init__(self, *, file_token: bytes, offset: int):
        self.file_token = file_token  # bytes
        self.offset = offset  # int

    @staticmethod
    def read(b: BytesIO, *args) -> "GetCdnFileHashes":
        # No flags
        
        file_token = Bytes.read(b)
        
        offset = Int.read(b)
        
        return GetCdnFileHashes(file_token=file_token, offset=offset)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(Bytes(self.file_token))
        
        b.write(Int(self.offset))
        
        return b.getvalue()
