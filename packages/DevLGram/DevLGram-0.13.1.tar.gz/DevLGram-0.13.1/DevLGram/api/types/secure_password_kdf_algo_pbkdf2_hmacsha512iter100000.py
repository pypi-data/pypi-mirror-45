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


class SecurePasswordKdfAlgoPBKDF2HMACSHA512iter100000(Object):
    """Attributes:
        ID: ``0xbbf2dda0``

    Args:
        salt: ``bytes``
    """

    __slots__ = ["salt"]

    ID = 0xbbf2dda0
    QUALNAME = "SecurePasswordKdfAlgoPBKDF2HMACSHA512iter100000"

    def __init__(self, *, salt: bytes):
        self.salt = salt  # bytes

    @staticmethod
    def read(b: BytesIO, *args) -> "SecurePasswordKdfAlgoPBKDF2HMACSHA512iter100000":
        # No flags
        
        salt = Bytes.read(b)
        
        return SecurePasswordKdfAlgoPBKDF2HMACSHA512iter100000(salt=salt)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(Bytes(self.salt))
        
        return b.getvalue()
