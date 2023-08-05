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


class InvokeWithMessagesRange(Object):
    """Attributes:
        ID: ``0x365275f2``

    Args:
        range: :obj:`MessageRange <DevLGram.api.types.MessageRange>`
        query: Any method from :obj:`DevLGram.api.functions`

    Raises:
        :obj:`RPCError <DevLGram.RPCError>`

    Returns:
        Any object from :obj:`DevLGram.api.types`
    """

    __slots__ = ["range", "query"]

    ID = 0x365275f2
    QUALNAME = "InvokeWithMessagesRange"

    def __init__(self, *, range, query):
        self.range = range  # MessageRange
        self.query = query  # !X

    @staticmethod
    def read(b: BytesIO, *args) -> "InvokeWithMessagesRange":
        # No flags
        
        range = Object.read(b)
        
        query = Object.read(b)
        
        return InvokeWithMessagesRange(range=range, query=query)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(self.range.write())
        
        b.write(self.query.write())
        
        return b.getvalue()
