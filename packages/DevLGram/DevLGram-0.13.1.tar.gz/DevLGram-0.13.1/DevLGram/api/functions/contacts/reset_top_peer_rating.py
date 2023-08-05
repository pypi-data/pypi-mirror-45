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


class ResetTopPeerRating(Object):
    """Attributes:
        ID: ``0x1ae373ac``

    Args:
        category: Either :obj:`TopPeerCategoryBotsPM <DevLGram.api.types.TopPeerCategoryBotsPM>`, :obj:`TopPeerCategoryBotsInline <DevLGram.api.types.TopPeerCategoryBotsInline>`, :obj:`TopPeerCategoryCorrespondents <DevLGram.api.types.TopPeerCategoryCorrespondents>`, :obj:`TopPeerCategoryGroups <DevLGram.api.types.TopPeerCategoryGroups>`, :obj:`TopPeerCategoryChannels <DevLGram.api.types.TopPeerCategoryChannels>` or :obj:`TopPeerCategoryPhoneCalls <DevLGram.api.types.TopPeerCategoryPhoneCalls>`
        peer: Either :obj:`InputPeerEmpty <DevLGram.api.types.InputPeerEmpty>`, :obj:`InputPeerSelf <DevLGram.api.types.InputPeerSelf>`, :obj:`InputPeerChat <DevLGram.api.types.InputPeerChat>`, :obj:`InputPeerUser <DevLGram.api.types.InputPeerUser>` or :obj:`InputPeerChannel <DevLGram.api.types.InputPeerChannel>`

    Raises:
        :obj:`RPCError <DevLGram.RPCError>`

    Returns:
        ``bool``
    """

    __slots__ = ["category", "peer"]

    ID = 0x1ae373ac
    QUALNAME = "contacts.ResetTopPeerRating"

    def __init__(self, *, category, peer):
        self.category = category  # TopPeerCategory
        self.peer = peer  # InputPeer

    @staticmethod
    def read(b: BytesIO, *args) -> "ResetTopPeerRating":
        # No flags
        
        category = Object.read(b)
        
        peer = Object.read(b)
        
        return ResetTopPeerRating(category=category, peer=peer)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(self.category.write())
        
        b.write(self.peer.write())
        
        return b.getvalue()
