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


class SetGameScore(Object):
    """Attributes:
        ID: ``0x8ef8ecc0``

    Args:
        peer: Either :obj:`InputPeerEmpty <DevLGram.api.types.InputPeerEmpty>`, :obj:`InputPeerSelf <DevLGram.api.types.InputPeerSelf>`, :obj:`InputPeerChat <DevLGram.api.types.InputPeerChat>`, :obj:`InputPeerUser <DevLGram.api.types.InputPeerUser>` or :obj:`InputPeerChannel <DevLGram.api.types.InputPeerChannel>`
        id: ``int`` ``32-bit``
        user_id: Either :obj:`InputUserEmpty <DevLGram.api.types.InputUserEmpty>`, :obj:`InputUserSelf <DevLGram.api.types.InputUserSelf>` or :obj:`InputUser <DevLGram.api.types.InputUser>`
        score: ``int`` ``32-bit``
        edit_message (optional): ``bool``
        force (optional): ``bool``

    Raises:
        :obj:`RPCError <DevLGram.RPCError>`

    Returns:
        Either :obj:`UpdatesTooLong <DevLGram.api.types.UpdatesTooLong>`, :obj:`UpdateShortMessage <DevLGram.api.types.UpdateShortMessage>`, :obj:`UpdateShortChatMessage <DevLGram.api.types.UpdateShortChatMessage>`, :obj:`UpdateShort <DevLGram.api.types.UpdateShort>`, :obj:`UpdatesCombined <DevLGram.api.types.UpdatesCombined>`, :obj:`Update <DevLGram.api.types.Update>` or :obj:`UpdateShortSentMessage <DevLGram.api.types.UpdateShortSentMessage>`
    """

    __slots__ = ["peer", "id", "user_id", "score", "edit_message", "force"]

    ID = 0x8ef8ecc0
    QUALNAME = "messages.SetGameScore"

    def __init__(self, *, peer, id: int, user_id, score: int, edit_message: bool = None, force: bool = None):
        self.edit_message = edit_message  # flags.0?true
        self.force = force  # flags.1?true
        self.peer = peer  # InputPeer
        self.id = id  # int
        self.user_id = user_id  # InputUser
        self.score = score  # int

    @staticmethod
    def read(b: BytesIO, *args) -> "SetGameScore":
        flags = Int.read(b)
        
        edit_message = True if flags & (1 << 0) else False
        force = True if flags & (1 << 1) else False
        peer = Object.read(b)
        
        id = Int.read(b)
        
        user_id = Object.read(b)
        
        score = Int.read(b)
        
        return SetGameScore(peer=peer, id=id, user_id=user_id, score=score, edit_message=edit_message, force=force)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        flags = 0
        flags |= (1 << 0) if self.edit_message is not None else 0
        flags |= (1 << 1) if self.force is not None else 0
        b.write(Int(flags))
        
        b.write(self.peer.write())
        
        b.write(Int(self.id))
        
        b.write(self.user_id.write())
        
        b.write(Int(self.score))
        
        return b.getvalue()
