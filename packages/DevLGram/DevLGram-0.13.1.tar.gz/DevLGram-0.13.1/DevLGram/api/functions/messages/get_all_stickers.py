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


class GetAllStickers(Object):
    """Attributes:
        ID: ``0x1c9618b1``

    Args:
        hash: ``int`` ``32-bit``

    Raises:
        :obj:`RPCError <DevLGram.RPCError>`

    Returns:
        Either :obj:`messages.AllStickersNotModified <DevLGram.api.types.messages.AllStickersNotModified>` or :obj:`messages.AllStickers <DevLGram.api.types.messages.AllStickers>`
    """

    __slots__ = ["hash"]

    ID = 0x1c9618b1
    QUALNAME = "messages.GetAllStickers"

    def __init__(self, *, hash: int):
        self.hash = hash  # int

    @staticmethod
    def read(b: BytesIO, *args) -> "GetAllStickers":
        # No flags
        
        hash = Int.read(b)
        
        return GetAllStickers(hash=hash)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(Int(self.hash))
        
        return b.getvalue()
