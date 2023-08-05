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


class CheckPassword(Object):
    """Attributes:
        ID: ``0xd18b4d16``

    Args:
        password: Either :obj:`InputCheckPasswordEmpty <DevLGram.api.types.InputCheckPasswordEmpty>` or :obj:`InputCheckPasswordSRP <DevLGram.api.types.InputCheckPasswordSRP>`

    Raises:
        :obj:`RPCError <DevLGram.RPCError>`

    Returns:
        :obj:`auth.Authorization <DevLGram.api.types.auth.Authorization>`
    """

    __slots__ = ["password"]

    ID = 0xd18b4d16
    QUALNAME = "auth.CheckPassword"

    def __init__(self, *, password):
        self.password = password  # InputCheckPasswordSRP

    @staticmethod
    def read(b: BytesIO, *args) -> "CheckPassword":
        # No flags
        
        password = Object.read(b)
        
        return CheckPassword(password=password)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(self.password.write())
        
        return b.getvalue()
