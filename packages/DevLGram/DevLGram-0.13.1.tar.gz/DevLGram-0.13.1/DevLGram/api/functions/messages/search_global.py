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


class SearchGlobal(Object):
    """Attributes:
        ID: ``0x9e3cacb0``

    Args:
        q: ``str``
        offset_date: ``int`` ``32-bit``
        offset_peer: Either :obj:`InputPeerEmpty <DevLGram.api.types.InputPeerEmpty>`, :obj:`InputPeerSelf <DevLGram.api.types.InputPeerSelf>`, :obj:`InputPeerChat <DevLGram.api.types.InputPeerChat>`, :obj:`InputPeerUser <DevLGram.api.types.InputPeerUser>` or :obj:`InputPeerChannel <DevLGram.api.types.InputPeerChannel>`
        offset_id: ``int`` ``32-bit``
        limit: ``int`` ``32-bit``

    Raises:
        :obj:`RPCError <DevLGram.RPCError>`

    Returns:
        Either :obj:`messages.Messages <DevLGram.api.types.messages.Messages>`, :obj:`messages.MessagesSlice <DevLGram.api.types.messages.MessagesSlice>`, :obj:`messages.ChannelMessages <DevLGram.api.types.messages.ChannelMessages>` or :obj:`messages.MessagesNotModified <DevLGram.api.types.messages.MessagesNotModified>`
    """

    __slots__ = ["q", "offset_date", "offset_peer", "offset_id", "limit"]

    ID = 0x9e3cacb0
    QUALNAME = "messages.SearchGlobal"

    def __init__(self, *, q: str, offset_date: int, offset_peer, offset_id: int, limit: int):
        self.q = q  # string
        self.offset_date = offset_date  # int
        self.offset_peer = offset_peer  # InputPeer
        self.offset_id = offset_id  # int
        self.limit = limit  # int

    @staticmethod
    def read(b: BytesIO, *args) -> "SearchGlobal":
        # No flags
        
        q = String.read(b)
        
        offset_date = Int.read(b)
        
        offset_peer = Object.read(b)
        
        offset_id = Int.read(b)
        
        limit = Int.read(b)
        
        return SearchGlobal(q=q, offset_date=offset_date, offset_peer=offset_peer, offset_id=offset_id, limit=limit)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(String(self.q))
        
        b.write(Int(self.offset_date))
        
        b.write(self.offset_peer.write())
        
        b.write(Int(self.offset_id))
        
        b.write(Int(self.limit))
        
        return b.getvalue()
