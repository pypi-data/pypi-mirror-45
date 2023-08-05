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


class SecureValueErrorData(Object):
    """Attributes:
        ID: ``0xe8a40bd9``

    Args:
        type: Either :obj:`SecureValueTypePersonalDetails <DevLGram.api.types.SecureValueTypePersonalDetails>`, :obj:`SecureValueTypePassport <DevLGram.api.types.SecureValueTypePassport>`, :obj:`SecureValueTypeDriverLicense <DevLGram.api.types.SecureValueTypeDriverLicense>`, :obj:`SecureValueTypeIdentityCard <DevLGram.api.types.SecureValueTypeIdentityCard>`, :obj:`SecureValueTypeInternalPassport <DevLGram.api.types.SecureValueTypeInternalPassport>`, :obj:`SecureValueTypeAddress <DevLGram.api.types.SecureValueTypeAddress>`, :obj:`SecureValueTypeUtilityBill <DevLGram.api.types.SecureValueTypeUtilityBill>`, :obj:`SecureValueTypeBankStatement <DevLGram.api.types.SecureValueTypeBankStatement>`, :obj:`SecureValueTypeRentalAgreement <DevLGram.api.types.SecureValueTypeRentalAgreement>`, :obj:`SecureValueTypePassportRegistration <DevLGram.api.types.SecureValueTypePassportRegistration>`, :obj:`SecureValueTypeTemporaryRegistration <DevLGram.api.types.SecureValueTypeTemporaryRegistration>`, :obj:`SecureValueTypePhone <DevLGram.api.types.SecureValueTypePhone>` or :obj:`SecureValueTypeEmail <DevLGram.api.types.SecureValueTypeEmail>`
        data_hash: ``bytes``
        field: ``str``
        text: ``str``
    """

    __slots__ = ["type", "data_hash", "field", "text"]

    ID = 0xe8a40bd9
    QUALNAME = "SecureValueErrorData"

    def __init__(self, *, type, data_hash: bytes, field: str, text: str):
        self.type = type  # SecureValueType
        self.data_hash = data_hash  # bytes
        self.field = field  # string
        self.text = text  # string

    @staticmethod
    def read(b: BytesIO, *args) -> "SecureValueErrorData":
        # No flags
        
        type = Object.read(b)
        
        data_hash = Bytes.read(b)
        
        field = String.read(b)
        
        text = String.read(b)
        
        return SecureValueErrorData(type=type, data_hash=data_hash, field=field, text=text)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(self.type.write())
        
        b.write(Bytes(self.data_hash))
        
        b.write(String(self.field))
        
        b.write(String(self.text))
        
        return b.getvalue()
