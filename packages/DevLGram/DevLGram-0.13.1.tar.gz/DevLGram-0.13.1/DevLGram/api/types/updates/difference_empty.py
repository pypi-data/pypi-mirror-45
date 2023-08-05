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


class DifferenceEmpty(Object):
    """Attributes:
        ID: ``0x5d75a138``

    Args:
        date: ``int`` ``32-bit``
        seq: ``int`` ``32-bit``

    See Also:
        This object can be returned by :obj:`updates.GetDifference <DevLGram.api.functions.updates.GetDifference>`.
    """

    __slots__ = ["date", "seq"]

    ID = 0x5d75a138
    QUALNAME = "updates.DifferenceEmpty"

    def __init__(self, *, date: int, seq: int):
        self.date = date  # int
        self.seq = seq  # int

    @staticmethod
    def read(b: BytesIO, *args) -> "DifferenceEmpty":
        # No flags
        
        date = Int.read(b)
        
        seq = Int.read(b)
        
        return DifferenceEmpty(date=date, seq=seq)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(Int(self.date))
        
        b.write(Int(self.seq))
        
        return b.getvalue()
