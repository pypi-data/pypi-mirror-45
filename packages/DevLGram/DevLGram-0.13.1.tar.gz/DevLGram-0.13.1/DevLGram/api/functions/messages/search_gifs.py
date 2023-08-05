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


class SearchGifs(Object):
    """Attributes:
        ID: ``0xbf9a776b``

    Args:
        q: ``str``
        offset: ``int`` ``32-bit``

    Raises:
        :obj:`RPCError <DevLGram.RPCError>`

    Returns:
        :obj:`messages.FoundGifs <DevLGram.api.types.messages.FoundGifs>`
    """

    __slots__ = ["q", "offset"]

    ID = 0xbf9a776b
    QUALNAME = "messages.SearchGifs"

    def __init__(self, *, q: str, offset: int):
        self.q = q  # string
        self.offset = offset  # int

    @staticmethod
    def read(b: BytesIO, *args) -> "SearchGifs":
        # No flags
        
        q = String.read(b)
        
        offset = Int.read(b)
        
        return SearchGifs(q=q, offset=offset)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(String(self.q))
        
        b.write(Int(self.offset))
        
        return b.getvalue()
