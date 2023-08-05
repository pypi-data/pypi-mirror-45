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


class WallPapers(Object):
    """Attributes:
        ID: ``0x702b65a9``

    Args:
        hash: ``int`` ``32-bit``
        wallpapers: List of :obj:`WallPaper <DevLGram.api.types.WallPaper>`

    See Also:
        This object can be returned by :obj:`account.GetWallPapers <DevLGram.api.functions.account.GetWallPapers>`.
    """

    __slots__ = ["hash", "wallpapers"]

    ID = 0x702b65a9
    QUALNAME = "account.WallPapers"

    def __init__(self, *, hash: int, wallpapers: list):
        self.hash = hash  # int
        self.wallpapers = wallpapers  # Vector<WallPaper>

    @staticmethod
    def read(b: BytesIO, *args) -> "WallPapers":
        # No flags
        
        hash = Int.read(b)
        
        wallpapers = Object.read(b)
        
        return WallPapers(hash=hash, wallpapers=wallpapers)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(Int(self.hash))
        
        b.write(Vector(self.wallpapers))
        
        return b.getvalue()
