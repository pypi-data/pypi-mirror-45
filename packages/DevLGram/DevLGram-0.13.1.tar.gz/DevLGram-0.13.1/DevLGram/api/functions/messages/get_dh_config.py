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


class GetDhConfig(Object):
    """Attributes:
        ID: ``0x26cf8950``

    Args:
        version: ``int`` ``32-bit``
        random_length: ``int`` ``32-bit``

    Raises:
        :obj:`RPCError <DevLGram.RPCError>`

    Returns:
        Either :obj:`messages.DhConfigNotModified <DevLGram.api.types.messages.DhConfigNotModified>` or :obj:`messages.DhConfig <DevLGram.api.types.messages.DhConfig>`
    """

    __slots__ = ["version", "random_length"]

    ID = 0x26cf8950
    QUALNAME = "messages.GetDhConfig"

    def __init__(self, *, version: int, random_length: int):
        self.version = version  # int
        self.random_length = random_length  # int

    @staticmethod
    def read(b: BytesIO, *args) -> "GetDhConfig":
        # No flags
        
        version = Int.read(b)
        
        random_length = Int.read(b)
        
        return GetDhConfig(version=version, random_length=random_length)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(Int(self.version))
        
        b.write(Int(self.random_length))
        
        return b.getvalue()
