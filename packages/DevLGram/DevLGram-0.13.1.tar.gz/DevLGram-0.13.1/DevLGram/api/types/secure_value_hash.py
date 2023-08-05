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


class SecureValueHash(Object):
    """Attributes:
        ID: ``0xed1ecdb0``

    Args:
        type: Either :obj:`SecureValueTypePersonalDetails <DevLGram.api.types.SecureValueTypePersonalDetails>`, :obj:`SecureValueTypePassport <DevLGram.api.types.SecureValueTypePassport>`, :obj:`SecureValueTypeDriverLicense <DevLGram.api.types.SecureValueTypeDriverLicense>`, :obj:`SecureValueTypeIdentityCard <DevLGram.api.types.SecureValueTypeIdentityCard>`, :obj:`SecureValueTypeInternalPassport <DevLGram.api.types.SecureValueTypeInternalPassport>`, :obj:`SecureValueTypeAddress <DevLGram.api.types.SecureValueTypeAddress>`, :obj:`SecureValueTypeUtilityBill <DevLGram.api.types.SecureValueTypeUtilityBill>`, :obj:`SecureValueTypeBankStatement <DevLGram.api.types.SecureValueTypeBankStatement>`, :obj:`SecureValueTypeRentalAgreement <DevLGram.api.types.SecureValueTypeRentalAgreement>`, :obj:`SecureValueTypePassportRegistration <DevLGram.api.types.SecureValueTypePassportRegistration>`, :obj:`SecureValueTypeTemporaryRegistration <DevLGram.api.types.SecureValueTypeTemporaryRegistration>`, :obj:`SecureValueTypePhone <DevLGram.api.types.SecureValueTypePhone>` or :obj:`SecureValueTypeEmail <DevLGram.api.types.SecureValueTypeEmail>`
        hash: ``bytes``
    """

    __slots__ = ["type", "hash"]

    ID = 0xed1ecdb0
    QUALNAME = "SecureValueHash"

    def __init__(self, *, type, hash: bytes):
        self.type = type  # SecureValueType
        self.hash = hash  # bytes

    @staticmethod
    def read(b: BytesIO, *args) -> "SecureValueHash":
        # No flags
        
        type = Object.read(b)
        
        hash = Bytes.read(b)
        
        return SecureValueHash(type=type, hash=hash)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(self.type.write())
        
        b.write(Bytes(self.hash))
        
        return b.getvalue()
