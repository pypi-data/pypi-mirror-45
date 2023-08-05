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


class GetGameHighScores(Object):
    """Attributes:
        ID: ``0xe822649d``

    Args:
        peer: Either :obj:`InputPeerEmpty <DevLGram.api.types.InputPeerEmpty>`, :obj:`InputPeerSelf <DevLGram.api.types.InputPeerSelf>`, :obj:`InputPeerChat <DevLGram.api.types.InputPeerChat>`, :obj:`InputPeerUser <DevLGram.api.types.InputPeerUser>` or :obj:`InputPeerChannel <DevLGram.api.types.InputPeerChannel>`
        id: ``int`` ``32-bit``
        user_id: Either :obj:`InputUserEmpty <DevLGram.api.types.InputUserEmpty>`, :obj:`InputUserSelf <DevLGram.api.types.InputUserSelf>` or :obj:`InputUser <DevLGram.api.types.InputUser>`

    Raises:
        :obj:`RPCError <DevLGram.RPCError>`

    Returns:
        :obj:`messages.HighScores <DevLGram.api.types.messages.HighScores>`
    """

    __slots__ = ["peer", "id", "user_id"]

    ID = 0xe822649d
    QUALNAME = "messages.GetGameHighScores"

    def __init__(self, *, peer, id: int, user_id):
        self.peer = peer  # InputPeer
        self.id = id  # int
        self.user_id = user_id  # InputUser

    @staticmethod
    def read(b: BytesIO, *args) -> "GetGameHighScores":
        # No flags
        
        peer = Object.read(b)
        
        id = Int.read(b)
        
        user_id = Object.read(b)
        
        return GetGameHighScores(peer=peer, id=id, user_id=user_id)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(self.peer.write())
        
        b.write(Int(self.id))
        
        b.write(self.user_id.write())
        
        return b.getvalue()
