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


class FavedStickers(Object):
    """Attributes:
        ID: ``0xf37f2f16``

    Args:
        hash: ``int`` ``32-bit``
        packs: List of :obj:`StickerPack <DevLGram.api.types.StickerPack>`
        stickers: List of either :obj:`DocumentEmpty <DevLGram.api.types.DocumentEmpty>` or :obj:`Document <DevLGram.api.types.Document>`

    See Also:
        This object can be returned by :obj:`messages.GetFavedStickers <DevLGram.api.functions.messages.GetFavedStickers>`.
    """

    __slots__ = ["hash", "packs", "stickers"]

    ID = 0xf37f2f16
    QUALNAME = "messages.FavedStickers"

    def __init__(self, *, hash: int, packs: list, stickers: list):
        self.hash = hash  # int
        self.packs = packs  # Vector<StickerPack>
        self.stickers = stickers  # Vector<Document>

    @staticmethod
    def read(b: BytesIO, *args) -> "FavedStickers":
        # No flags
        
        hash = Int.read(b)
        
        packs = Object.read(b)
        
        stickers = Object.read(b)
        
        return FavedStickers(hash=hash, packs=packs, stickers=stickers)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(Int(self.hash))
        
        b.write(Vector(self.packs))
        
        b.write(Vector(self.stickers))
        
        return b.getvalue()
