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


class StickerSetCovered(Object):
    """Attributes:
        ID: ``0x6410a5d2``

    Args:
        set: :obj:`StickerSet <DevLGram.api.types.StickerSet>`
        cover: Either :obj:`DocumentEmpty <DevLGram.api.types.DocumentEmpty>` or :obj:`Document <DevLGram.api.types.Document>`

    See Also:
        This object can be returned by :obj:`messages.GetAttachedStickers <DevLGram.api.functions.messages.GetAttachedStickers>`.
    """

    __slots__ = ["set", "cover"]

    ID = 0x6410a5d2
    QUALNAME = "StickerSetCovered"

    def __init__(self, *, set, cover):
        self.set = set  # StickerSet
        self.cover = cover  # Document

    @staticmethod
    def read(b: BytesIO, *args) -> "StickerSetCovered":
        # No flags
        
        set = Object.read(b)
        
        cover = Object.read(b)
        
        return StickerSetCovered(set=set, cover=cover)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(self.set.write())
        
        b.write(self.cover.write())
        
        return b.getvalue()
