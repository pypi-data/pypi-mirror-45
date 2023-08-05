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


class TopPeer(Object):
    """Attributes:
        ID: ``0xedcdc05b``

    Args:
        peer: Either :obj:`PeerUser <DevLGram.api.types.PeerUser>`, :obj:`PeerChat <DevLGram.api.types.PeerChat>` or :obj:`PeerChannel <DevLGram.api.types.PeerChannel>`
        rating: ``float`` ``64-bit``
    """

    __slots__ = ["peer", "rating"]

    ID = 0xedcdc05b
    QUALNAME = "TopPeer"

    def __init__(self, *, peer, rating: float):
        self.peer = peer  # Peer
        self.rating = rating  # double

    @staticmethod
    def read(b: BytesIO, *args) -> "TopPeer":
        # No flags
        
        peer = Object.read(b)
        
        rating = Double.read(b)
        
        return TopPeer(peer=peer, rating=rating)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(self.peer.write())
        
        b.write(Double(self.rating))
        
        return b.getvalue()
