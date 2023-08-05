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


class ArchivedStickers(Object):
    """Attributes:
        ID: ``0x4fcba9c8``

    Args:
        count: ``int`` ``32-bit``
        sets: List of either :obj:`StickerSetCovered <DevLGram.api.types.StickerSetCovered>` or :obj:`StickerSetMultiCovered <DevLGram.api.types.StickerSetMultiCovered>`

    See Also:
        This object can be returned by :obj:`messages.GetArchivedStickers <DevLGram.api.functions.messages.GetArchivedStickers>`.
    """

    __slots__ = ["count", "sets"]

    ID = 0x4fcba9c8
    QUALNAME = "messages.ArchivedStickers"

    def __init__(self, *, count: int, sets: list):
        self.count = count  # int
        self.sets = sets  # Vector<StickerSetCovered>

    @staticmethod
    def read(b: BytesIO, *args) -> "ArchivedStickers":
        # No flags
        
        count = Int.read(b)
        
        sets = Object.read(b)
        
        return ArchivedStickers(count=count, sets=sets)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(Int(self.count))
        
        b.write(Vector(self.sets))
        
        return b.getvalue()
