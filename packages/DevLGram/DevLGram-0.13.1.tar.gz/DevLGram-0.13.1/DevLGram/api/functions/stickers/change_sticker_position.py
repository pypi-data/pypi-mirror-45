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


class ChangeStickerPosition(Object):
    """Attributes:
        ID: ``0xffb6d4ca``

    Args:
        sticker: Either :obj:`InputDocumentEmpty <DevLGram.api.types.InputDocumentEmpty>` or :obj:`InputDocument <DevLGram.api.types.InputDocument>`
        position: ``int`` ``32-bit``

    Raises:
        :obj:`RPCError <DevLGram.RPCError>`

    Returns:
        :obj:`messages.StickerSet <DevLGram.api.types.messages.StickerSet>`
    """

    __slots__ = ["sticker", "position"]

    ID = 0xffb6d4ca
    QUALNAME = "stickers.ChangeStickerPosition"

    def __init__(self, *, sticker, position: int):
        self.sticker = sticker  # InputDocument
        self.position = position  # int

    @staticmethod
    def read(b: BytesIO, *args) -> "ChangeStickerPosition":
        # No flags
        
        sticker = Object.read(b)
        
        position = Int.read(b)
        
        return ChangeStickerPosition(sticker=sticker, position=position)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(self.sticker.write())
        
        b.write(Int(self.position))
        
        return b.getvalue()
