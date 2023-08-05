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


class Report(Object):
    """Attributes:
        ID: ``0xbd82b658``

    Args:
        peer: Either :obj:`InputPeerEmpty <DevLGram.api.types.InputPeerEmpty>`, :obj:`InputPeerSelf <DevLGram.api.types.InputPeerSelf>`, :obj:`InputPeerChat <DevLGram.api.types.InputPeerChat>`, :obj:`InputPeerUser <DevLGram.api.types.InputPeerUser>` or :obj:`InputPeerChannel <DevLGram.api.types.InputPeerChannel>`
        id: List of ``int`` ``32-bit``
        reason: Either :obj:`InputReportReasonSpam <DevLGram.api.types.InputReportReasonSpam>`, :obj:`InputReportReasonViolence <DevLGram.api.types.InputReportReasonViolence>`, :obj:`InputReportReasonPornography <DevLGram.api.types.InputReportReasonPornography>`, :obj:`InputReportReasonChildAbuse <DevLGram.api.types.InputReportReasonChildAbuse>`, :obj:`InputReportReasonOther <DevLGram.api.types.InputReportReasonOther>` or :obj:`InputReportReasonCopyright <DevLGram.api.types.InputReportReasonCopyright>`

    Raises:
        :obj:`RPCError <DevLGram.RPCError>`

    Returns:
        ``bool``
    """

    __slots__ = ["peer", "id", "reason"]

    ID = 0xbd82b658
    QUALNAME = "messages.Report"

    def __init__(self, *, peer, id: list, reason):
        self.peer = peer  # InputPeer
        self.id = id  # Vector<int>
        self.reason = reason  # ReportReason

    @staticmethod
    def read(b: BytesIO, *args) -> "Report":
        # No flags
        
        peer = Object.read(b)
        
        id = Object.read(b, Int)
        
        reason = Object.read(b)
        
        return Report(peer=peer, id=id, reason=reason)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(self.peer.write())
        
        b.write(Vector(self.id, Int))
        
        b.write(self.reason.write())
        
        return b.getvalue()
