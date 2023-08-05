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


class PageTableRow(Object):
    """Attributes:
        ID: ``0xe0c0c5e5``

    Args:
        cells: List of :obj:`PageTableCell <DevLGram.api.types.PageTableCell>`
    """

    __slots__ = ["cells"]

    ID = 0xe0c0c5e5
    QUALNAME = "PageTableRow"

    def __init__(self, *, cells: list):
        self.cells = cells  # Vector<PageTableCell>

    @staticmethod
    def read(b: BytesIO, *args) -> "PageTableRow":
        # No flags
        
        cells = Object.read(b)
        
        return PageTableRow(cells=cells)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(Vector(self.cells))
        
        return b.getvalue()
