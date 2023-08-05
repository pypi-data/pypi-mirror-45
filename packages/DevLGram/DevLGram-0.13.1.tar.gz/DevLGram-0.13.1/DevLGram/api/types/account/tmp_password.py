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


class TmpPassword(Object):
    """Attributes:
        ID: ``0xdb64fd34``

    Args:
        tmp_password: ``bytes``
        valid_until: ``int`` ``32-bit``

    See Also:
        This object can be returned by :obj:`account.GetTmpPassword <DevLGram.api.functions.account.GetTmpPassword>`.
    """

    __slots__ = ["tmp_password", "valid_until"]

    ID = 0xdb64fd34
    QUALNAME = "account.TmpPassword"

    def __init__(self, *, tmp_password: bytes, valid_until: int):
        self.tmp_password = tmp_password  # bytes
        self.valid_until = valid_until  # int

    @staticmethod
    def read(b: BytesIO, *args) -> "TmpPassword":
        # No flags
        
        tmp_password = Bytes.read(b)
        
        valid_until = Int.read(b)
        
        return TmpPassword(tmp_password=tmp_password, valid_until=valid_until)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(Bytes(self.tmp_password))
        
        b.write(Int(self.valid_until))
        
        return b.getvalue()
