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


class UpdateNotifySettings(Object):
    """Attributes:
        ID: ``0x84be5b93``

    Args:
        peer: Either :obj:`InputNotifyPeer <DevLGram.api.types.InputNotifyPeer>`, :obj:`InputNotifyUsers <DevLGram.api.types.InputNotifyUsers>`, :obj:`InputNotifyChats <DevLGram.api.types.InputNotifyChats>` or :obj:`InputNotifyBroadcasts <DevLGram.api.types.InputNotifyBroadcasts>`
        settings: :obj:`InputPeerNotifySettings <DevLGram.api.types.InputPeerNotifySettings>`

    Raises:
        :obj:`RPCError <DevLGram.RPCError>`

    Returns:
        ``bool``
    """

    __slots__ = ["peer", "settings"]

    ID = 0x84be5b93
    QUALNAME = "account.UpdateNotifySettings"

    def __init__(self, *, peer, settings):
        self.peer = peer  # InputNotifyPeer
        self.settings = settings  # InputPeerNotifySettings

    @staticmethod
    def read(b: BytesIO, *args) -> "UpdateNotifySettings":
        # No flags
        
        peer = Object.read(b)
        
        settings = Object.read(b)
        
        return UpdateNotifySettings(peer=peer, settings=settings)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(self.peer.write())
        
        b.write(self.settings.write())
        
        return b.getvalue()
