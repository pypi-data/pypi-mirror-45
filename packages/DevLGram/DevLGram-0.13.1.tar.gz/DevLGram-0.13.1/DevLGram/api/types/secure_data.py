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


class SecureData(Object):
    """Attributes:
        ID: ``0x8aeabec3``

    Args:
        data: ``bytes``
        data_hash: ``bytes``
        secret: ``bytes``
    """

    __slots__ = ["data", "data_hash", "secret"]

    ID = 0x8aeabec3
    QUALNAME = "SecureData"

    def __init__(self, *, data: bytes, data_hash: bytes, secret: bytes):
        self.data = data  # bytes
        self.data_hash = data_hash  # bytes
        self.secret = secret  # bytes

    @staticmethod
    def read(b: BytesIO, *args) -> "SecureData":
        # No flags
        
        data = Bytes.read(b)
        
        data_hash = Bytes.read(b)
        
        secret = Bytes.read(b)
        
        return SecureData(data=data, data_hash=data_hash, secret=secret)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(Bytes(self.data))
        
        b.write(Bytes(self.data_hash))
        
        b.write(Bytes(self.secret))
        
        return b.getvalue()
