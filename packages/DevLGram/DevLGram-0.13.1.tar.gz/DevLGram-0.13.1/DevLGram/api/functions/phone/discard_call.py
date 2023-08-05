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


class DiscardCall(Object):
    """Attributes:
        ID: ``0x78d413a6``

    Args:
        peer: :obj:`InputPhoneCall <DevLGram.api.types.InputPhoneCall>`
        duration: ``int`` ``32-bit``
        reason: Either :obj:`PhoneCallDiscardReasonMissed <DevLGram.api.types.PhoneCallDiscardReasonMissed>`, :obj:`PhoneCallDiscardReasonDisconnect <DevLGram.api.types.PhoneCallDiscardReasonDisconnect>`, :obj:`PhoneCallDiscardReasonHangup <DevLGram.api.types.PhoneCallDiscardReasonHangup>` or :obj:`PhoneCallDiscardReasonBusy <DevLGram.api.types.PhoneCallDiscardReasonBusy>`
        connection_id: ``int`` ``64-bit``

    Raises:
        :obj:`RPCError <DevLGram.RPCError>`

    Returns:
        Either :obj:`UpdatesTooLong <DevLGram.api.types.UpdatesTooLong>`, :obj:`UpdateShortMessage <DevLGram.api.types.UpdateShortMessage>`, :obj:`UpdateShortChatMessage <DevLGram.api.types.UpdateShortChatMessage>`, :obj:`UpdateShort <DevLGram.api.types.UpdateShort>`, :obj:`UpdatesCombined <DevLGram.api.types.UpdatesCombined>`, :obj:`Update <DevLGram.api.types.Update>` or :obj:`UpdateShortSentMessage <DevLGram.api.types.UpdateShortSentMessage>`
    """

    __slots__ = ["peer", "duration", "reason", "connection_id"]

    ID = 0x78d413a6
    QUALNAME = "phone.DiscardCall"

    def __init__(self, *, peer, duration: int, reason, connection_id: int):
        self.peer = peer  # InputPhoneCall
        self.duration = duration  # int
        self.reason = reason  # PhoneCallDiscardReason
        self.connection_id = connection_id  # long

    @staticmethod
    def read(b: BytesIO, *args) -> "DiscardCall":
        # No flags
        
        peer = Object.read(b)
        
        duration = Int.read(b)
        
        reason = Object.read(b)
        
        connection_id = Long.read(b)
        
        return DiscardCall(peer=peer, duration=duration, reason=reason, connection_id=connection_id)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(self.peer.write())
        
        b.write(Int(self.duration))
        
        b.write(self.reason.write())
        
        b.write(Long(self.connection_id))
        
        return b.getvalue()
