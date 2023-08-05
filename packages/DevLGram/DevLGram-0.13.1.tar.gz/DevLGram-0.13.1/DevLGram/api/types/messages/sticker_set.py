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


class StickerSet(Object):
    """Attributes:
        ID: ``0xb60a24a6``

    Args:
        set: :obj:`StickerSet <DevLGram.api.types.StickerSet>`
        packs: List of :obj:`StickerPack <DevLGram.api.types.StickerPack>`
        documents: List of either :obj:`DocumentEmpty <DevLGram.api.types.DocumentEmpty>` or :obj:`Document <DevLGram.api.types.Document>`

    See Also:
        This object can be returned by :obj:`messages.GetStickerSet <DevLGram.api.functions.messages.GetStickerSet>`, :obj:`stickers.CreateStickerSet <DevLGram.api.functions.stickers.CreateStickerSet>`, :obj:`stickers.RemoveStickerFromSet <DevLGram.api.functions.stickers.RemoveStickerFromSet>`, :obj:`stickers.ChangeStickerPosition <DevLGram.api.functions.stickers.ChangeStickerPosition>` and :obj:`stickers.AddStickerToSet <DevLGram.api.functions.stickers.AddStickerToSet>`.
    """

    __slots__ = ["set", "packs", "documents"]

    ID = 0xb60a24a6
    QUALNAME = "messages.StickerSet"

    def __init__(self, *, set, packs: list, documents: list):
        self.set = set  # StickerSet
        self.packs = packs  # Vector<StickerPack>
        self.documents = documents  # Vector<Document>

    @staticmethod
    def read(b: BytesIO, *args) -> "StickerSet":
        # No flags
        
        set = Object.read(b)
        
        packs = Object.read(b)
        
        documents = Object.read(b)
        
        return StickerSet(set=set, packs=packs, documents=documents)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(self.set.write())
        
        b.write(Vector(self.packs))
        
        b.write(Vector(self.documents))
        
        return b.getvalue()
