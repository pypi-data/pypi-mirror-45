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


class RpcAnswerDropped(Object):
    """Attributes:
        ID: ``0xa43ad8b7``

    Args:
        msg_id: ``int`` ``64-bit``
        seq_no: ``int`` ``32-bit``
        bytes: ``int`` ``32-bit``

    See Also:
        This object can be returned by :obj:`RpcDropAnswer <DevLGram.api.functions.RpcDropAnswer>`.
    """

    __slots__ = ["msg_id", "seq_no", "bytes"]

    ID = 0xa43ad8b7
    QUALNAME = "RpcAnswerDropped"

    def __init__(self, *, msg_id: int, seq_no: int, bytes: int):
        self.msg_id = msg_id  # long
        self.seq_no = seq_no  # int
        self.bytes = bytes  # int

    @staticmethod
    def read(b: BytesIO, *args) -> "RpcAnswerDropped":
        # No flags
        
        msg_id = Long.read(b)
        
        seq_no = Int.read(b)
        
        bytes = Int.read(b)
        
        return RpcAnswerDropped(msg_id=msg_id, seq_no=seq_no, bytes=bytes)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(Long(self.msg_id))
        
        b.write(Int(self.seq_no))
        
        b.write(Int(self.bytes))
        
        return b.getvalue()
