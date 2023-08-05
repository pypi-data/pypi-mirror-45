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


class GetPaymentForm(Object):
    """Attributes:
        ID: ``0x99f09745``

    Args:
        msg_id: ``int`` ``32-bit``

    Raises:
        :obj:`RPCError <DevLGram.RPCError>`

    Returns:
        :obj:`payments.PaymentForm <DevLGram.api.types.payments.PaymentForm>`
    """

    __slots__ = ["msg_id"]

    ID = 0x99f09745
    QUALNAME = "payments.GetPaymentForm"

    def __init__(self, *, msg_id: int):
        self.msg_id = msg_id  # int

    @staticmethod
    def read(b: BytesIO, *args) -> "GetPaymentForm":
        # No flags
        
        msg_id = Int.read(b)
        
        return GetPaymentForm(msg_id=msg_id)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(Int(self.msg_id))
        
        return b.getvalue()
