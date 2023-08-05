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


class AddStickerToSet(Object):
    """Attributes:
        ID: ``0x8653febe``

    Args:
        stickerset: Either :obj:`InputStickerSetEmpty <DevLGram.api.types.InputStickerSetEmpty>`, :obj:`InputStickerSetID <DevLGram.api.types.InputStickerSetID>` or :obj:`InputStickerSetShortName <DevLGram.api.types.InputStickerSetShortName>`
        sticker: :obj:`InputStickerSetItem <DevLGram.api.types.InputStickerSetItem>`

    Raises:
        :obj:`RPCError <DevLGram.RPCError>`

    Returns:
        :obj:`messages.StickerSet <DevLGram.api.types.messages.StickerSet>`
    """

    __slots__ = ["stickerset", "sticker"]

    ID = 0x8653febe
    QUALNAME = "stickers.AddStickerToSet"

    def __init__(self, *, stickerset, sticker):
        self.stickerset = stickerset  # InputStickerSet
        self.sticker = sticker  # InputStickerSetItem

    @staticmethod
    def read(b: BytesIO, *args) -> "AddStickerToSet":
        # No flags
        
        stickerset = Object.read(b)
        
        sticker = Object.read(b)
        
        return AddStickerToSet(stickerset=stickerset, sticker=sticker)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(self.stickerset.write())
        
        b.write(self.sticker.write())
        
        return b.getvalue()
