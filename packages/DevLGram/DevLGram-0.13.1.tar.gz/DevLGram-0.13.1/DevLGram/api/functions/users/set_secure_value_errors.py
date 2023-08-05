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


class SetSecureValueErrors(Object):
    """Attributes:
        ID: ``0x90c894b5``

    Args:
        id: Either :obj:`InputUserEmpty <DevLGram.api.types.InputUserEmpty>`, :obj:`InputUserSelf <DevLGram.api.types.InputUserSelf>` or :obj:`InputUser <DevLGram.api.types.InputUser>`
        errors: List of either :obj:`SecureValueErrorData <DevLGram.api.types.SecureValueErrorData>`, :obj:`SecureValueErrorFrontSide <DevLGram.api.types.SecureValueErrorFrontSide>`, :obj:`SecureValueErrorReverseSide <DevLGram.api.types.SecureValueErrorReverseSide>`, :obj:`SecureValueErrorSelfie <DevLGram.api.types.SecureValueErrorSelfie>`, :obj:`SecureValueErrorFile <DevLGram.api.types.SecureValueErrorFile>`, :obj:`SecureValueErrorFiles <DevLGram.api.types.SecureValueErrorFiles>`, :obj:`SecureValueError <DevLGram.api.types.SecureValueError>`, :obj:`SecureValueErrorTranslationFile <DevLGram.api.types.SecureValueErrorTranslationFile>` or :obj:`SecureValueErrorTranslationFiles <DevLGram.api.types.SecureValueErrorTranslationFiles>`

    Raises:
        :obj:`RPCError <DevLGram.RPCError>`

    Returns:
        ``bool``
    """

    __slots__ = ["id", "errors"]

    ID = 0x90c894b5
    QUALNAME = "users.SetSecureValueErrors"

    def __init__(self, *, id, errors: list):
        self.id = id  # InputUser
        self.errors = errors  # Vector<SecureValueError>

    @staticmethod
    def read(b: BytesIO, *args) -> "SetSecureValueErrors":
        # No flags
        
        id = Object.read(b)
        
        errors = Object.read(b)
        
        return SetSecureValueErrors(id=id, errors=errors)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(self.id.write())
        
        b.write(Vector(self.errors))
        
        return b.getvalue()
