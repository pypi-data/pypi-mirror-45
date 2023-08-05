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


class ReadHistory(Object):
    """Attributes:
        ID: ``0x0e306d3a``

    Args:
        peer: Either :obj:`InputPeerEmpty <DevLGram.api.types.InputPeerEmpty>`, :obj:`InputPeerSelf <DevLGram.api.types.InputPeerSelf>`, :obj:`InputPeerChat <DevLGram.api.types.InputPeerChat>`, :obj:`InputPeerUser <DevLGram.api.types.InputPeerUser>` or :obj:`InputPeerChannel <DevLGram.api.types.InputPeerChannel>`
        max_id: ``int`` ``32-bit``

    Raises:
        :obj:`RPCError <DevLGram.RPCError>`

    Returns:
        :obj:`messages.AffectedMessages <DevLGram.api.types.messages.AffectedMessages>`
    """

    __slots__ = ["peer", "max_id"]

    ID = 0x0e306d3a
    QUALNAME = "messages.ReadHistory"

    def __init__(self, *, peer, max_id: int):
        self.peer = peer  # InputPeer
        self.max_id = max_id  # int

    @staticmethod
    def read(b: BytesIO, *args) -> "ReadHistory":
        # No flags
        
        peer = Object.read(b)
        
        max_id = Int.read(b)
        
        return ReadHistory(peer=peer, max_id=max_id)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(self.peer.write())
        
        b.write(Int(self.max_id))
        
        return b.getvalue()
