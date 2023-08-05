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


class GetNotifyExceptions(Object):
    """Attributes:
        ID: ``0x53577479``

    Args:
        compare_sound (optional): ``bool``
        peer (optional): Either :obj:`InputNotifyPeer <DevLGram.api.types.InputNotifyPeer>`, :obj:`InputNotifyUsers <DevLGram.api.types.InputNotifyUsers>`, :obj:`InputNotifyChats <DevLGram.api.types.InputNotifyChats>` or :obj:`InputNotifyBroadcasts <DevLGram.api.types.InputNotifyBroadcasts>`

    Raises:
        :obj:`RPCError <DevLGram.RPCError>`

    Returns:
        Either :obj:`UpdatesTooLong <DevLGram.api.types.UpdatesTooLong>`, :obj:`UpdateShortMessage <DevLGram.api.types.UpdateShortMessage>`, :obj:`UpdateShortChatMessage <DevLGram.api.types.UpdateShortChatMessage>`, :obj:`UpdateShort <DevLGram.api.types.UpdateShort>`, :obj:`UpdatesCombined <DevLGram.api.types.UpdatesCombined>`, :obj:`Update <DevLGram.api.types.Update>` or :obj:`UpdateShortSentMessage <DevLGram.api.types.UpdateShortSentMessage>`
    """

    __slots__ = ["compare_sound", "peer"]

    ID = 0x53577479
    QUALNAME = "account.GetNotifyExceptions"

    def __init__(self, *, compare_sound: bool = None, peer=None):
        self.compare_sound = compare_sound  # flags.1?true
        self.peer = peer  # flags.0?InputNotifyPeer

    @staticmethod
    def read(b: BytesIO, *args) -> "GetNotifyExceptions":
        flags = Int.read(b)
        
        compare_sound = True if flags & (1 << 1) else False
        peer = Object.read(b) if flags & (1 << 0) else None
        
        return GetNotifyExceptions(compare_sound=compare_sound, peer=peer)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        flags = 0
        flags |= (1 << 1) if self.compare_sound is not None else 0
        flags |= (1 << 0) if self.peer is not None else 0
        b.write(Int(flags))
        
        if self.peer is not None:
            b.write(self.peer.write())
        
        return b.getvalue()
