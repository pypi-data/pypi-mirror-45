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


class Ping(Object):
    """Attributes:
        ID: ``0x7abe77ec``

    Args:
        ping_id: ``int`` ``64-bit``

    Raises:
        :obj:`RPCError <DevLGram.RPCError>`

    Returns:
        :obj:`Pong <DevLGram.api.types.Pong>`
    """

    __slots__ = ["ping_id"]

    ID = 0x7abe77ec
    QUALNAME = "Ping"

    def __init__(self, *, ping_id: int):
        self.ping_id = ping_id  # long

    @staticmethod
    def read(b: BytesIO, *args) -> "Ping":
        # No flags
        
        ping_id = Long.read(b)
        
        return Ping(ping_id=ping_id)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(Long(self.ping_id))
        
        return b.getvalue()
