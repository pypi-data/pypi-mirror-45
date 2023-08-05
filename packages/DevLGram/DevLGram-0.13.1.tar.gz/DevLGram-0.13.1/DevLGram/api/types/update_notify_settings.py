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
        ID: ``0xbec268ef``

    Args:
        peer: Either :obj:`NotifyPeer <DevLGram.api.types.NotifyPeer>`, :obj:`NotifyUsers <DevLGram.api.types.NotifyUsers>`, :obj:`NotifyChats <DevLGram.api.types.NotifyChats>` or :obj:`NotifyBroadcasts <DevLGram.api.types.NotifyBroadcasts>`
        notify_settings: :obj:`PeerNotifySettings <DevLGram.api.types.PeerNotifySettings>`
    """

    __slots__ = ["peer", "notify_settings"]

    ID = 0xbec268ef
    QUALNAME = "UpdateNotifySettings"

    def __init__(self, *, peer, notify_settings):
        self.peer = peer  # NotifyPeer
        self.notify_settings = notify_settings  # PeerNotifySettings

    @staticmethod
    def read(b: BytesIO, *args) -> "UpdateNotifySettings":
        # No flags
        
        peer = Object.read(b)
        
        notify_settings = Object.read(b)
        
        return UpdateNotifySettings(peer=peer, notify_settings=notify_settings)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(self.peer.write())
        
        b.write(self.notify_settings.write())
        
        return b.getvalue()
