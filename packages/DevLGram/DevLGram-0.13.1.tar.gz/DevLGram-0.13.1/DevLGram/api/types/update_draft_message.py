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


class UpdateDraftMessage(Object):
    """Attributes:
        ID: ``0xee2bb969``

    Args:
        peer: Either :obj:`PeerUser <DevLGram.api.types.PeerUser>`, :obj:`PeerChat <DevLGram.api.types.PeerChat>` or :obj:`PeerChannel <DevLGram.api.types.PeerChannel>`
        draft: Either :obj:`DraftMessageEmpty <DevLGram.api.types.DraftMessageEmpty>` or :obj:`DraftMessage <DevLGram.api.types.DraftMessage>`
    """

    __slots__ = ["peer", "draft"]

    ID = 0xee2bb969
    QUALNAME = "UpdateDraftMessage"

    def __init__(self, *, peer, draft):
        self.peer = peer  # Peer
        self.draft = draft  # DraftMessage

    @staticmethod
    def read(b: BytesIO, *args) -> "UpdateDraftMessage":
        # No flags
        
        peer = Object.read(b)
        
        draft = Object.read(b)
        
        return UpdateDraftMessage(peer=peer, draft=draft)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(self.peer.write())
        
        b.write(self.draft.write())
        
        return b.getvalue()
