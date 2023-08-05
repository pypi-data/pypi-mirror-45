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


class SecureRequiredType(Object):
    """Attributes:
        ID: ``0x829d99da``

    Args:
        type: Either :obj:`SecureValueTypePersonalDetails <DevLGram.api.types.SecureValueTypePersonalDetails>`, :obj:`SecureValueTypePassport <DevLGram.api.types.SecureValueTypePassport>`, :obj:`SecureValueTypeDriverLicense <DevLGram.api.types.SecureValueTypeDriverLicense>`, :obj:`SecureValueTypeIdentityCard <DevLGram.api.types.SecureValueTypeIdentityCard>`, :obj:`SecureValueTypeInternalPassport <DevLGram.api.types.SecureValueTypeInternalPassport>`, :obj:`SecureValueTypeAddress <DevLGram.api.types.SecureValueTypeAddress>`, :obj:`SecureValueTypeUtilityBill <DevLGram.api.types.SecureValueTypeUtilityBill>`, :obj:`SecureValueTypeBankStatement <DevLGram.api.types.SecureValueTypeBankStatement>`, :obj:`SecureValueTypeRentalAgreement <DevLGram.api.types.SecureValueTypeRentalAgreement>`, :obj:`SecureValueTypePassportRegistration <DevLGram.api.types.SecureValueTypePassportRegistration>`, :obj:`SecureValueTypeTemporaryRegistration <DevLGram.api.types.SecureValueTypeTemporaryRegistration>`, :obj:`SecureValueTypePhone <DevLGram.api.types.SecureValueTypePhone>` or :obj:`SecureValueTypeEmail <DevLGram.api.types.SecureValueTypeEmail>`
        native_names (optional): ``bool``
        selfie_required (optional): ``bool``
        translation_required (optional): ``bool``
    """

    __slots__ = ["type", "native_names", "selfie_required", "translation_required"]

    ID = 0x829d99da
    QUALNAME = "SecureRequiredType"

    def __init__(self, *, type, native_names: bool = None, selfie_required: bool = None, translation_required: bool = None):
        self.native_names = native_names  # flags.0?true
        self.selfie_required = selfie_required  # flags.1?true
        self.translation_required = translation_required  # flags.2?true
        self.type = type  # SecureValueType

    @staticmethod
    def read(b: BytesIO, *args) -> "SecureRequiredType":
        flags = Int.read(b)
        
        native_names = True if flags & (1 << 0) else False
        selfie_required = True if flags & (1 << 1) else False
        translation_required = True if flags & (1 << 2) else False
        type = Object.read(b)
        
        return SecureRequiredType(type=type, native_names=native_names, selfie_required=selfie_required, translation_required=translation_required)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        flags = 0
        flags |= (1 << 0) if self.native_names is not None else 0
        flags |= (1 << 1) if self.selfie_required is not None else 0
        flags |= (1 << 2) if self.translation_required is not None else 0
        b.write(Int(flags))
        
        b.write(self.type.write())
        
        return b.getvalue()
