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


class ReqPqMulti(Object):
    """Attributes:
        ID: ``0xbe7e8ef1``

    Args:
        nonce: ``int`` ``128-bit``

    Raises:
        :obj:`RPCError <DevLGram.RPCError>`

    Returns:
        :obj:`ResPQ <DevLGram.api.types.ResPQ>`
    """

    __slots__ = ["nonce"]

    ID = 0xbe7e8ef1
    QUALNAME = "ReqPqMulti"

    def __init__(self, *, nonce: int):
        self.nonce = nonce  # int128

    @staticmethod
    def read(b: BytesIO, *args) -> "ReqPqMulti":
        # No flags
        
        nonce = Int128.read(b)
        
        return ReqPqMulti(nonce=nonce)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(Int128(self.nonce))
        
        return b.getvalue()
