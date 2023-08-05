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


class ChannelAdminLogEventActionChangeStickerSet(Object):
    """Attributes:
        ID: ``0xb1c3caa7``

    Args:
        prev_stickerset: Either :obj:`InputStickerSetEmpty <DevLGram.api.types.InputStickerSetEmpty>`, :obj:`InputStickerSetID <DevLGram.api.types.InputStickerSetID>` or :obj:`InputStickerSetShortName <DevLGram.api.types.InputStickerSetShortName>`
        new_stickerset: Either :obj:`InputStickerSetEmpty <DevLGram.api.types.InputStickerSetEmpty>`, :obj:`InputStickerSetID <DevLGram.api.types.InputStickerSetID>` or :obj:`InputStickerSetShortName <DevLGram.api.types.InputStickerSetShortName>`
    """

    __slots__ = ["prev_stickerset", "new_stickerset"]

    ID = 0xb1c3caa7
    QUALNAME = "ChannelAdminLogEventActionChangeStickerSet"

    def __init__(self, *, prev_stickerset, new_stickerset):
        self.prev_stickerset = prev_stickerset  # InputStickerSet
        self.new_stickerset = new_stickerset  # InputStickerSet

    @staticmethod
    def read(b: BytesIO, *args) -> "ChannelAdminLogEventActionChangeStickerSet":
        # No flags
        
        prev_stickerset = Object.read(b)
        
        new_stickerset = Object.read(b)
        
        return ChannelAdminLogEventActionChangeStickerSet(prev_stickerset=prev_stickerset, new_stickerset=new_stickerset)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(self.prev_stickerset.write())
        
        b.write(self.new_stickerset.write())
        
        return b.getvalue()
