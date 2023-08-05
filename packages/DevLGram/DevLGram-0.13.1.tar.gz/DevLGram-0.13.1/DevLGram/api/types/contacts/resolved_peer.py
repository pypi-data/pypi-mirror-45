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


class ResolvedPeer(Object):
    """Attributes:
        ID: ``0x7f077ad9``

    Args:
        peer: Either :obj:`PeerUser <DevLGram.api.types.PeerUser>`, :obj:`PeerChat <DevLGram.api.types.PeerChat>` or :obj:`PeerChannel <DevLGram.api.types.PeerChannel>`
        chats: List of either :obj:`ChatEmpty <DevLGram.api.types.ChatEmpty>`, :obj:`Chat <DevLGram.api.types.Chat>`, :obj:`ChatForbidden <DevLGram.api.types.ChatForbidden>`, :obj:`Channel <DevLGram.api.types.Channel>` or :obj:`ChannelForbidden <DevLGram.api.types.ChannelForbidden>`
        users: List of either :obj:`UserEmpty <DevLGram.api.types.UserEmpty>` or :obj:`User <DevLGram.api.types.User>`

    See Also:
        This object can be returned by :obj:`contacts.ResolveUsername <DevLGram.api.functions.contacts.ResolveUsername>`.
    """

    __slots__ = ["peer", "chats", "users"]

    ID = 0x7f077ad9
    QUALNAME = "contacts.ResolvedPeer"

    def __init__(self, *, peer, chats: list, users: list):
        self.peer = peer  # Peer
        self.chats = chats  # Vector<Chat>
        self.users = users  # Vector<User>

    @staticmethod
    def read(b: BytesIO, *args) -> "ResolvedPeer":
        # No flags
        
        peer = Object.read(b)
        
        chats = Object.read(b)
        
        users = Object.read(b)
        
        return ResolvedPeer(peer=peer, chats=chats, users=users)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(self.peer.write())
        
        b.write(Vector(self.chats))
        
        b.write(Vector(self.users))
        
        return b.getvalue()
