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


class ReadEncryptedHistory(Object):
    """Attributes:
        ID: ``0x7f4b690a``

    Args:
        peer: :obj:`InputEncryptedChat <DevLGram.api.types.InputEncryptedChat>`
        max_date: ``int`` ``32-bit``

    Raises:
        :obj:`RPCError <DevLGram.RPCError>`

    Returns:
        ``bool``
    """

    __slots__ = ["peer", "max_date"]

    ID = 0x7f4b690a
    QUALNAME = "messages.ReadEncryptedHistory"

    def __init__(self, *, peer, max_date: int):
        self.peer = peer  # InputEncryptedChat
        self.max_date = max_date  # int

    @staticmethod
    def read(b: BytesIO, *args) -> "ReadEncryptedHistory":
        # No flags
        
        peer = Object.read(b)
        
        max_date = Int.read(b)
        
        return ReadEncryptedHistory(peer=peer, max_date=max_date)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(self.peer.write())
        
        b.write(Int(self.max_date))
        
        return b.getvalue()
