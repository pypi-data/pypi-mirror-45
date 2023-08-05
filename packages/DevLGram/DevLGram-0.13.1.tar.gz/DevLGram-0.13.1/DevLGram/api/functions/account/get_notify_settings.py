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


class GetNotifySettings(Object):
    """Attributes:
        ID: ``0x12b3ad31``

    Args:
        peer: Either :obj:`InputNotifyPeer <DevLGram.api.types.InputNotifyPeer>`, :obj:`InputNotifyUsers <DevLGram.api.types.InputNotifyUsers>`, :obj:`InputNotifyChats <DevLGram.api.types.InputNotifyChats>` or :obj:`InputNotifyBroadcasts <DevLGram.api.types.InputNotifyBroadcasts>`

    Raises:
        :obj:`RPCError <DevLGram.RPCError>`

    Returns:
        :obj:`PeerNotifySettings <DevLGram.api.types.PeerNotifySettings>`
    """

    __slots__ = ["peer"]

    ID = 0x12b3ad31
    QUALNAME = "account.GetNotifySettings"

    def __init__(self, *, peer):
        self.peer = peer  # InputNotifyPeer

    @staticmethod
    def read(b: BytesIO, *args) -> "GetNotifySettings":
        # No flags
        
        peer = Object.read(b)
        
        return GetNotifySettings(peer=peer)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(self.peer.write())
        
        return b.getvalue()
