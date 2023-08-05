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


class SentCode(Object):
    """Attributes:
        ID: ``0x38faab5f``

    Args:
        type: Either :obj:`auth.SentCodeTypeApp <DevLGram.api.types.auth.SentCodeTypeApp>`, :obj:`auth.SentCodeTypeSms <DevLGram.api.types.auth.SentCodeTypeSms>`, :obj:`auth.SentCodeTypeCall <DevLGram.api.types.auth.SentCodeTypeCall>` or :obj:`auth.SentCodeTypeFlashCall <DevLGram.api.types.auth.SentCodeTypeFlashCall>`
        phone_code_hash: ``str``
        phone_registered (optional): ``bool``
        next_type (optional): Either :obj:`auth.CodeTypeSms <DevLGram.api.types.auth.CodeTypeSms>`, :obj:`auth.CodeTypeCall <DevLGram.api.types.auth.CodeTypeCall>` or :obj:`auth.CodeTypeFlashCall <DevLGram.api.types.auth.CodeTypeFlashCall>`
        timeout (optional): ``int`` ``32-bit``
        terms_of_service (optional): :obj:`help.TermsOfService <DevLGram.api.types.help.TermsOfService>`

    See Also:
        This object can be returned by :obj:`auth.SendCode <DevLGram.api.functions.auth.SendCode>`, :obj:`auth.ResendCode <DevLGram.api.functions.auth.ResendCode>`, :obj:`account.SendChangePhoneCode <DevLGram.api.functions.account.SendChangePhoneCode>`, :obj:`account.SendConfirmPhoneCode <DevLGram.api.functions.account.SendConfirmPhoneCode>` and :obj:`account.SendVerifyPhoneCode <DevLGram.api.functions.account.SendVerifyPhoneCode>`.
    """

    __slots__ = ["type", "phone_code_hash", "phone_registered", "next_type", "timeout", "terms_of_service"]

    ID = 0x38faab5f
    QUALNAME = "auth.SentCode"

    def __init__(self, *, type, phone_code_hash: str, phone_registered: bool = None, next_type=None, timeout: int = None, terms_of_service=None):
        self.phone_registered = phone_registered  # flags.0?true
        self.type = type  # auth.SentCodeType
        self.phone_code_hash = phone_code_hash  # string
        self.next_type = next_type  # flags.1?auth.CodeType
        self.timeout = timeout  # flags.2?int
        self.terms_of_service = terms_of_service  # flags.3?help.TermsOfService

    @staticmethod
    def read(b: BytesIO, *args) -> "SentCode":
        flags = Int.read(b)
        
        phone_registered = True if flags & (1 << 0) else False
        type = Object.read(b)
        
        phone_code_hash = String.read(b)
        
        next_type = Object.read(b) if flags & (1 << 1) else None
        
        timeout = Int.read(b) if flags & (1 << 2) else None
        terms_of_service = Object.read(b) if flags & (1 << 3) else None
        
        return SentCode(type=type, phone_code_hash=phone_code_hash, phone_registered=phone_registered, next_type=next_type, timeout=timeout, terms_of_service=terms_of_service)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        flags = 0
        flags |= (1 << 0) if self.phone_registered is not None else 0
        flags |= (1 << 1) if self.next_type is not None else 0
        flags |= (1 << 2) if self.timeout is not None else 0
        flags |= (1 << 3) if self.terms_of_service is not None else 0
        b.write(Int(flags))
        
        b.write(self.type.write())
        
        b.write(String(self.phone_code_hash))
        
        if self.next_type is not None:
            b.write(self.next_type.write())
        
        if self.timeout is not None:
            b.write(Int(self.timeout))
        
        if self.terms_of_service is not None:
            b.write(self.terms_of_service.write())
        
        return b.getvalue()
