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


class InvokeAfterMsg(Object):
    """Attributes:
        ID: ``0xcb9f372d``

    Args:
        msg_id: ``int`` ``64-bit``
        query: Any method from :obj:`DevLGram.api.functions`

    Raises:
        :obj:`RPCError <DevLGram.RPCError>`

    Returns:
        Any object from :obj:`DevLGram.api.types`
    """

    __slots__ = ["msg_id", "query"]

    ID = 0xcb9f372d
    QUALNAME = "InvokeAfterMsg"

    def __init__(self, *, msg_id: int, query):
        self.msg_id = msg_id  # long
        self.query = query  # !X

    @staticmethod
    def read(b: BytesIO, *args) -> "InvokeAfterMsg":
        # No flags
        
        msg_id = Long.read(b)
        
        query = Object.read(b)
        
        return InvokeAfterMsg(msg_id=msg_id, query=query)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(Long(self.msg_id))
        
        b.write(self.query.write())
        
        return b.getvalue()
