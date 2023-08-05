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


class PageBlockOrderedList(Object):
    """Attributes:
        ID: ``0x9a8ae1e1``

    Args:
        items: List of either :obj:`PageListOrderedItemText <DevLGram.api.types.PageListOrderedItemText>` or :obj:`PageListOrderedItemBlocks <DevLGram.api.types.PageListOrderedItemBlocks>`
    """

    __slots__ = ["items"]

    ID = 0x9a8ae1e1
    QUALNAME = "PageBlockOrderedList"

    def __init__(self, *, items: list):
        self.items = items  # Vector<PageListOrderedItem>

    @staticmethod
    def read(b: BytesIO, *args) -> "PageBlockOrderedList":
        # No flags
        
        items = Object.read(b)
        
        return PageBlockOrderedList(items=items)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(Vector(self.items))
        
        return b.getvalue()
