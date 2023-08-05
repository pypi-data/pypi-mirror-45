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


class RemoveStickerFromSet(Object):
    """Attributes:
        ID: ``0xf7760f51``

    Args:
        sticker: Either :obj:`InputDocumentEmpty <DevLGram.api.types.InputDocumentEmpty>` or :obj:`InputDocument <DevLGram.api.types.InputDocument>`

    Raises:
        :obj:`RPCError <DevLGram.RPCError>`

    Returns:
        :obj:`messages.StickerSet <DevLGram.api.types.messages.StickerSet>`
    """

    __slots__ = ["sticker"]

    ID = 0xf7760f51
    QUALNAME = "stickers.RemoveStickerFromSet"

    def __init__(self, *, sticker):
        self.sticker = sticker  # InputDocument

    @staticmethod
    def read(b: BytesIO, *args) -> "RemoveStickerFromSet":
        # No flags
        
        sticker = Object.read(b)
        
        return RemoveStickerFromSet(sticker=sticker)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(self.sticker.write())
        
        return b.getvalue()
