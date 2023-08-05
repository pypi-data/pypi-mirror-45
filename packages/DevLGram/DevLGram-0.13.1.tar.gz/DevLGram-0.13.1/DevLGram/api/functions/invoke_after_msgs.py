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


class InvokeAfterMsgs(Object):
    """Attributes:
        ID: ``0x3dc4b4f0``

    Args:
        msg_ids: List of ``int`` ``64-bit``
        query: Any method from :obj:`DevLGram.api.functions`

    Raises:
        :obj:`RPCError <DevLGram.RPCError>`

    Returns:
        Any object from :obj:`DevLGram.api.types`
    """

    __slots__ = ["msg_ids", "query"]

    ID = 0x3dc4b4f0
    QUALNAME = "InvokeAfterMsgs"

    def __init__(self, *, msg_ids: list, query):
        self.msg_ids = msg_ids  # Vector<long>
        self.query = query  # !X

    @staticmethod
    def read(b: BytesIO, *args) -> "InvokeAfterMsgs":
        # No flags
        
        msg_ids = Object.read(b, Long)
        
        query = Object.read(b)
        
        return InvokeAfterMsgs(msg_ids=msg_ids, query=query)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(Vector(self.msg_ids, Long))
        
        b.write(self.query.write())
        
        return b.getvalue()
