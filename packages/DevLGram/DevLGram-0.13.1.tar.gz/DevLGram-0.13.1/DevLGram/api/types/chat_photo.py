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


class ChatPhoto(Object):
    """Attributes:
        ID: ``0x6153276a``

    Args:
        photo_small: Either :obj:`FileLocationUnavailable <DevLGram.api.types.FileLocationUnavailable>` or :obj:`FileLocation <DevLGram.api.types.FileLocation>`
        photo_big: Either :obj:`FileLocationUnavailable <DevLGram.api.types.FileLocationUnavailable>` or :obj:`FileLocation <DevLGram.api.types.FileLocation>`
    """

    __slots__ = ["photo_small", "photo_big"]

    ID = 0x6153276a
    QUALNAME = "ChatPhoto"

    def __init__(self, *, photo_small, photo_big):
        self.photo_small = photo_small  # FileLocation
        self.photo_big = photo_big  # FileLocation

    @staticmethod
    def read(b: BytesIO, *args) -> "ChatPhoto":
        # No flags
        
        photo_small = Object.read(b)
        
        photo_big = Object.read(b)
        
        return ChatPhoto(photo_small=photo_small, photo_big=photo_big)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(self.photo_small.write())
        
        b.write(self.photo_big.write())
        
        return b.getvalue()
