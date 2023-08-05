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


class UpdateUserPhone(Object):
    """Attributes:
        ID: ``0x12b9417b``

    Args:
        user_id: ``int`` ``32-bit``
        phone: ``str``
    """

    __slots__ = ["user_id", "phone"]

    ID = 0x12b9417b
    QUALNAME = "UpdateUserPhone"

    def __init__(self, *, user_id: int, phone: str):
        self.user_id = user_id  # int
        self.phone = phone  # string

    @staticmethod
    def read(b: BytesIO, *args) -> "UpdateUserPhone":
        # No flags
        
        user_id = Int.read(b)
        
        phone = String.read(b)
        
        return UpdateUserPhone(user_id=user_id, phone=phone)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(Int(self.user_id))
        
        b.write(String(self.phone))
        
        return b.getvalue()
