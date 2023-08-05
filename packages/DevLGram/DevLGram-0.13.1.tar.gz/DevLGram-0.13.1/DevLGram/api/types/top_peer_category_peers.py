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


class TopPeerCategoryPeers(Object):
    """Attributes:
        ID: ``0xfb834291``

    Args:
        category: Either :obj:`TopPeerCategoryBotsPM <DevLGram.api.types.TopPeerCategoryBotsPM>`, :obj:`TopPeerCategoryBotsInline <DevLGram.api.types.TopPeerCategoryBotsInline>`, :obj:`TopPeerCategoryCorrespondents <DevLGram.api.types.TopPeerCategoryCorrespondents>`, :obj:`TopPeerCategoryGroups <DevLGram.api.types.TopPeerCategoryGroups>`, :obj:`TopPeerCategoryChannels <DevLGram.api.types.TopPeerCategoryChannels>` or :obj:`TopPeerCategoryPhoneCalls <DevLGram.api.types.TopPeerCategoryPhoneCalls>`
        count: ``int`` ``32-bit``
        peers: List of :obj:`TopPeer <DevLGram.api.types.TopPeer>`
    """

    __slots__ = ["category", "count", "peers"]

    ID = 0xfb834291
    QUALNAME = "TopPeerCategoryPeers"

    def __init__(self, *, category, count: int, peers: list):
        self.category = category  # TopPeerCategory
        self.count = count  # int
        self.peers = peers  # Vector<TopPeer>

    @staticmethod
    def read(b: BytesIO, *args) -> "TopPeerCategoryPeers":
        # No flags
        
        category = Object.read(b)
        
        count = Int.read(b)
        
        peers = Object.read(b)
        
        return TopPeerCategoryPeers(category=category, count=count, peers=peers)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(self.category.write())
        
        b.write(Int(self.count))
        
        b.write(Vector(self.peers))
        
        return b.getvalue()
