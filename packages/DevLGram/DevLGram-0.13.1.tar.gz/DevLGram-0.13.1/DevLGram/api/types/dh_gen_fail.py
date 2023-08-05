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


class DhGenFail(Object):
    """Attributes:
        ID: ``0xa69dae02``

    Args:
        nonce: ``int`` ``128-bit``
        server_nonce: ``int`` ``128-bit``
        new_nonce_hash3: ``int`` ``128-bit``

    See Also:
        This object can be returned by :obj:`SetClientDHParams <DevLGram.api.functions.SetClientDHParams>`.
    """

    __slots__ = ["nonce", "server_nonce", "new_nonce_hash3"]

    ID = 0xa69dae02
    QUALNAME = "DhGenFail"

    def __init__(self, *, nonce: int, server_nonce: int, new_nonce_hash3: int):
        self.nonce = nonce  # int128
        self.server_nonce = server_nonce  # int128
        self.new_nonce_hash3 = new_nonce_hash3  # int128

    @staticmethod
    def read(b: BytesIO, *args) -> "DhGenFail":
        # No flags
        
        nonce = Int128.read(b)
        
        server_nonce = Int128.read(b)
        
        new_nonce_hash3 = Int128.read(b)
        
        return DhGenFail(nonce=nonce, server_nonce=server_nonce, new_nonce_hash3=new_nonce_hash3)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(Int128(self.nonce))
        
        b.write(Int128(self.server_nonce))
        
        b.write(Int128(self.new_nonce_hash3))
        
        return b.getvalue()
