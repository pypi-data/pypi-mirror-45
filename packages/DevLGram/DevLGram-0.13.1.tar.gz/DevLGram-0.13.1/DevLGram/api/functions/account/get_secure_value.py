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


class GetSecureValue(Object):
    """Attributes:
        ID: ``0x73665bc2``

    Args:
        types: List of either :obj:`SecureValueTypePersonalDetails <DevLGram.api.types.SecureValueTypePersonalDetails>`, :obj:`SecureValueTypePassport <DevLGram.api.types.SecureValueTypePassport>`, :obj:`SecureValueTypeDriverLicense <DevLGram.api.types.SecureValueTypeDriverLicense>`, :obj:`SecureValueTypeIdentityCard <DevLGram.api.types.SecureValueTypeIdentityCard>`, :obj:`SecureValueTypeInternalPassport <DevLGram.api.types.SecureValueTypeInternalPassport>`, :obj:`SecureValueTypeAddress <DevLGram.api.types.SecureValueTypeAddress>`, :obj:`SecureValueTypeUtilityBill <DevLGram.api.types.SecureValueTypeUtilityBill>`, :obj:`SecureValueTypeBankStatement <DevLGram.api.types.SecureValueTypeBankStatement>`, :obj:`SecureValueTypeRentalAgreement <DevLGram.api.types.SecureValueTypeRentalAgreement>`, :obj:`SecureValueTypePassportRegistration <DevLGram.api.types.SecureValueTypePassportRegistration>`, :obj:`SecureValueTypeTemporaryRegistration <DevLGram.api.types.SecureValueTypeTemporaryRegistration>`, :obj:`SecureValueTypePhone <DevLGram.api.types.SecureValueTypePhone>` or :obj:`SecureValueTypeEmail <DevLGram.api.types.SecureValueTypeEmail>`

    Raises:
        :obj:`RPCError <DevLGram.RPCError>`

    Returns:
        List of :obj:`SecureValue <DevLGram.api.types.SecureValue>`
    """

    __slots__ = ["types"]

    ID = 0x73665bc2
    QUALNAME = "account.GetSecureValue"

    def __init__(self, *, types: list):
        self.types = types  # Vector<SecureValueType>

    @staticmethod
    def read(b: BytesIO, *args) -> "GetSecureValue":
        # No flags
        
        types = Object.read(b)
        
        return GetSecureValue(types=types)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(Vector(self.types))
        
        return b.getvalue()
