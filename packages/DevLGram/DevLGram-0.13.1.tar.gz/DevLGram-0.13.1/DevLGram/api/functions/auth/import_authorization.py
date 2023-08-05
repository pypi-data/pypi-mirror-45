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


class ImportAuthorization(Object):
    """Attributes:
        ID: ``0xe3ef9613``

    Args:
        id: ``int`` ``32-bit``
        bytes: ``bytes``

    Raises:
        :obj:`RPCError <DevLGram.RPCError>`

    Returns:
        :obj:`auth.Authorization <DevLGram.api.types.auth.Authorization>`
    """

    __slots__ = ["id", "bytes"]

    ID = 0xe3ef9613
    QUALNAME = "auth.ImportAuthorization"

    def __init__(self, *, id: int, bytes: bytes):
        self.id = id  # int
        self.bytes = bytes  # bytes

    @staticmethod
    def read(b: BytesIO, *args) -> "ImportAuthorization":
        # No flags
        
        id = Int.read(b)
        
        bytes = Bytes.read(b)
        
        return ImportAuthorization(id=id, bytes=bytes)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(Int(self.id))
        
        b.write(Bytes(self.bytes))
        
        return b.getvalue()
