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


class PaymentReceipt(Object):
    """Attributes:
        ID: ``0x500911e1``

    Args:
        date: ``int`` ``32-bit``
        bot_id: ``int`` ``32-bit``
        invoice: :obj:`Invoice <DevLGram.api.types.Invoice>`
        provider_id: ``int`` ``32-bit``
        currency: ``str``
        total_amount: ``int`` ``64-bit``
        credentials_title: ``str``
        users: List of either :obj:`UserEmpty <DevLGram.api.types.UserEmpty>` or :obj:`User <DevLGram.api.types.User>`
        info (optional): :obj:`PaymentRequestedInfo <DevLGram.api.types.PaymentRequestedInfo>`
        shipping (optional): :obj:`ShippingOption <DevLGram.api.types.ShippingOption>`

    See Also:
        This object can be returned by :obj:`payments.GetPaymentReceipt <DevLGram.api.functions.payments.GetPaymentReceipt>`.
    """

    __slots__ = ["date", "bot_id", "invoice", "provider_id", "currency", "total_amount", "credentials_title", "users", "info", "shipping"]

    ID = 0x500911e1
    QUALNAME = "payments.PaymentReceipt"

    def __init__(self, *, date: int, bot_id: int, invoice, provider_id: int, currency: str, total_amount: int, credentials_title: str, users: list, info=None, shipping=None):
        self.date = date  # int
        self.bot_id = bot_id  # int
        self.invoice = invoice  # Invoice
        self.provider_id = provider_id  # int
        self.info = info  # flags.0?PaymentRequestedInfo
        self.shipping = shipping  # flags.1?ShippingOption
        self.currency = currency  # string
        self.total_amount = total_amount  # long
        self.credentials_title = credentials_title  # string
        self.users = users  # Vector<User>

    @staticmethod
    def read(b: BytesIO, *args) -> "PaymentReceipt":
        flags = Int.read(b)
        
        date = Int.read(b)
        
        bot_id = Int.read(b)
        
        invoice = Object.read(b)
        
        provider_id = Int.read(b)
        
        info = Object.read(b) if flags & (1 << 0) else None
        
        shipping = Object.read(b) if flags & (1 << 1) else None
        
        currency = String.read(b)
        
        total_amount = Long.read(b)
        
        credentials_title = String.read(b)
        
        users = Object.read(b)
        
        return PaymentReceipt(date=date, bot_id=bot_id, invoice=invoice, provider_id=provider_id, currency=currency, total_amount=total_amount, credentials_title=credentials_title, users=users, info=info, shipping=shipping)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        flags = 0
        flags |= (1 << 0) if self.info is not None else 0
        flags |= (1 << 1) if self.shipping is not None else 0
        b.write(Int(flags))
        
        b.write(Int(self.date))
        
        b.write(Int(self.bot_id))
        
        b.write(self.invoice.write())
        
        b.write(Int(self.provider_id))
        
        if self.info is not None:
            b.write(self.info.write())
        
        if self.shipping is not None:
            b.write(self.shipping.write())
        
        b.write(String(self.currency))
        
        b.write(Long(self.total_amount))
        
        b.write(String(self.credentials_title))
        
        b.write(Vector(self.users))
        
        return b.getvalue()
