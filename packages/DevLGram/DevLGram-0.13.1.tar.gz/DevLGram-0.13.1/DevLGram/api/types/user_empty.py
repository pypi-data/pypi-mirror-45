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


class UserEmpty(Object):
    """Attributes:
        ID: ``0x200250ba``

    Args:
        id: ``int`` ``32-bit``

    See Also:
        This object can be returned by :obj:`account.UpdateProfile <DevLGram.api.functions.account.UpdateProfile>`, :obj:`account.UpdateUsername <DevLGram.api.functions.account.UpdateUsername>`, :obj:`account.ChangePhone <DevLGram.api.functions.account.ChangePhone>` and :obj:`users.GetUsers <DevLGram.api.functions.users.GetUsers>`.
    """

    __slots__ = ["id"]

    ID = 0x200250ba
    QUALNAME = "UserEmpty"

    def __init__(self, *, id: int):
        self.id = id  # int

    @staticmethod
    def read(b: BytesIO, *args) -> "UserEmpty":
        # No flags
        
        id = Int.read(b)
        
        return UserEmpty(id=id)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(Int(self.id))
        
        return b.getvalue()
