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


class GetFile(Object):
    """Attributes:
        ID: ``0xe3a6cfb5``

    Args:
        location: Either :obj:`InputFileLocation <DevLGram.api.types.InputFileLocation>`, :obj:`InputEncryptedFileLocation <DevLGram.api.types.InputEncryptedFileLocation>`, :obj:`InputDocumentFileLocation <DevLGram.api.types.InputDocumentFileLocation>`, :obj:`InputSecureFileLocation <DevLGram.api.types.InputSecureFileLocation>` or :obj:`InputTakeoutFileLocation <DevLGram.api.types.InputTakeoutFileLocation>`
        offset: ``int`` ``32-bit``
        limit: ``int`` ``32-bit``

    Raises:
        :obj:`RPCError <DevLGram.RPCError>`

    Returns:
        Either :obj:`upload.File <DevLGram.api.types.upload.File>` or :obj:`upload.FileCdnRedirect <DevLGram.api.types.upload.FileCdnRedirect>`
    """

    __slots__ = ["location", "offset", "limit"]

    ID = 0xe3a6cfb5
    QUALNAME = "upload.GetFile"

    def __init__(self, *, location, offset: int, limit: int):
        self.location = location  # InputFileLocation
        self.offset = offset  # int
        self.limit = limit  # int

    @staticmethod
    def read(b: BytesIO, *args) -> "GetFile":
        # No flags
        
        location = Object.read(b)
        
        offset = Int.read(b)
        
        limit = Int.read(b)
        
        return GetFile(location=location, offset=offset, limit=limit)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(self.location.write())
        
        b.write(Int(self.offset))
        
        b.write(Int(self.limit))
        
        return b.getvalue()
