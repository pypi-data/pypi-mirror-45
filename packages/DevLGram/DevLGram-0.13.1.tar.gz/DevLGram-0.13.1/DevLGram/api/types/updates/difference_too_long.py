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


class DifferenceTooLong(Object):
    """Attributes:
        ID: ``0x4afe8f6d``

    Args:
        pts: ``int`` ``32-bit``

    See Also:
        This object can be returned by :obj:`updates.GetDifference <DevLGram.api.functions.updates.GetDifference>`.
    """

    __slots__ = ["pts"]

    ID = 0x4afe8f6d
    QUALNAME = "updates.DifferenceTooLong"

    def __init__(self, *, pts: int):
        self.pts = pts  # int

    @staticmethod
    def read(b: BytesIO, *args) -> "DifferenceTooLong":
        # No flags
        
        pts = Int.read(b)
        
        return DifferenceTooLong(pts=pts)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(Int(self.pts))
        
        return b.getvalue()
