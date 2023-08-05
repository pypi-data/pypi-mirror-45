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


class UpdatePasswordSettings(Object):
    """Attributes:
        ID: ``0xa59b102f``

    Args:
        password: Either :obj:`InputCheckPasswordEmpty <DevLGram.api.types.InputCheckPasswordEmpty>` or :obj:`InputCheckPasswordSRP <DevLGram.api.types.InputCheckPasswordSRP>`
        new_settings: :obj:`account.PasswordInputSettings <DevLGram.api.types.account.PasswordInputSettings>`

    Raises:
        :obj:`RPCError <DevLGram.RPCError>`

    Returns:
        ``bool``
    """

    __slots__ = ["password", "new_settings"]

    ID = 0xa59b102f
    QUALNAME = "account.UpdatePasswordSettings"

    def __init__(self, *, password, new_settings):
        self.password = password  # InputCheckPasswordSRP
        self.new_settings = new_settings  # account.PasswordInputSettings

    @staticmethod
    def read(b: BytesIO, *args) -> "UpdatePasswordSettings":
        # No flags
        
        password = Object.read(b)
        
        new_settings = Object.read(b)
        
        return UpdatePasswordSettings(password=password, new_settings=new_settings)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(self.password.write())
        
        b.write(self.new_settings.write())
        
        return b.getvalue()
