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


class Stickers(Object):
    """Attributes:
        ID: ``0xe4599bbd``

    Args:
        hash: ``int`` ``32-bit``
        stickers: List of either :obj:`DocumentEmpty <DevLGram.api.types.DocumentEmpty>` or :obj:`Document <DevLGram.api.types.Document>`

    See Also:
        This object can be returned by :obj:`messages.GetStickers <DevLGram.api.functions.messages.GetStickers>`.
    """

    __slots__ = ["hash", "stickers"]

    ID = 0xe4599bbd
    QUALNAME = "messages.Stickers"

    def __init__(self, *, hash: int, stickers: list):
        self.hash = hash  # int
        self.stickers = stickers  # Vector<Document>

    @staticmethod
    def read(b: BytesIO, *args) -> "Stickers":
        # No flags
        
        hash = Int.read(b)
        
        stickers = Object.read(b)
        
        return Stickers(hash=hash, stickers=stickers)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(Int(self.hash))
        
        b.write(Vector(self.stickers))
        
        return b.getvalue()
