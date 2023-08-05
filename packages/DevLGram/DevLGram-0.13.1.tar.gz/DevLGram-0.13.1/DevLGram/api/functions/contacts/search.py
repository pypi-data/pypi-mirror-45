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


class Search(Object):
    """Attributes:
        ID: ``0x11f812d8``

    Args:
        q: ``str``
        limit: ``int`` ``32-bit``

    Raises:
        :obj:`RPCError <DevLGram.RPCError>`

    Returns:
        :obj:`contacts.Found <DevLGram.api.types.contacts.Found>`
    """

    __slots__ = ["q", "limit"]

    ID = 0x11f812d8
    QUALNAME = "contacts.Search"

    def __init__(self, *, q: str, limit: int):
        self.q = q  # string
        self.limit = limit  # int

    @staticmethod
    def read(b: BytesIO, *args) -> "Search":
        # No flags
        
        q = String.read(b)
        
        limit = Int.read(b)
        
        return Search(q=q, limit=limit)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(String(self.q))
        
        b.write(Int(self.limit))
        
        return b.getvalue()
