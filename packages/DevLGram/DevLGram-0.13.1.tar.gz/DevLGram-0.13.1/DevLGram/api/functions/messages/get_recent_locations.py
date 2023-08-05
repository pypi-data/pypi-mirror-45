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


class GetRecentLocations(Object):
    """Attributes:
        ID: ``0xbbc45b09``

    Args:
        peer: Either :obj:`InputPeerEmpty <DevLGram.api.types.InputPeerEmpty>`, :obj:`InputPeerSelf <DevLGram.api.types.InputPeerSelf>`, :obj:`InputPeerChat <DevLGram.api.types.InputPeerChat>`, :obj:`InputPeerUser <DevLGram.api.types.InputPeerUser>` or :obj:`InputPeerChannel <DevLGram.api.types.InputPeerChannel>`
        limit: ``int`` ``32-bit``
        hash: ``int`` ``32-bit``

    Raises:
        :obj:`RPCError <DevLGram.RPCError>`

    Returns:
        Either :obj:`messages.Messages <DevLGram.api.types.messages.Messages>`, :obj:`messages.MessagesSlice <DevLGram.api.types.messages.MessagesSlice>`, :obj:`messages.ChannelMessages <DevLGram.api.types.messages.ChannelMessages>` or :obj:`messages.MessagesNotModified <DevLGram.api.types.messages.MessagesNotModified>`
    """

    __slots__ = ["peer", "limit", "hash"]

    ID = 0xbbc45b09
    QUALNAME = "messages.GetRecentLocations"

    def __init__(self, *, peer, limit: int, hash: int):
        self.peer = peer  # InputPeer
        self.limit = limit  # int
        self.hash = hash  # int

    @staticmethod
    def read(b: BytesIO, *args) -> "GetRecentLocations":
        # No flags
        
        peer = Object.read(b)
        
        limit = Int.read(b)
        
        hash = Int.read(b)
        
        return GetRecentLocations(peer=peer, limit=limit, hash=hash)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(self.peer.write())
        
        b.write(Int(self.limit))
        
        b.write(Int(self.hash))
        
        return b.getvalue()
