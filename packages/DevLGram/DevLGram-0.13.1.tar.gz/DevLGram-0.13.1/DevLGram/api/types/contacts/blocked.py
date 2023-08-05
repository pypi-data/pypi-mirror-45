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


class Blocked(Object):
    """Attributes:
        ID: ``0x1c138d15``

    Args:
        blocked: List of :obj:`ContactBlocked <DevLGram.api.types.ContactBlocked>`
        users: List of either :obj:`UserEmpty <DevLGram.api.types.UserEmpty>` or :obj:`User <DevLGram.api.types.User>`

    See Also:
        This object can be returned by :obj:`contacts.GetBlocked <DevLGram.api.functions.contacts.GetBlocked>`.
    """

    __slots__ = ["blocked", "users"]

    ID = 0x1c138d15
    QUALNAME = "contacts.Blocked"

    def __init__(self, *, blocked: list, users: list):
        self.blocked = blocked  # Vector<ContactBlocked>
        self.users = users  # Vector<User>

    @staticmethod
    def read(b: BytesIO, *args) -> "Blocked":
        # No flags
        
        blocked = Object.read(b)
        
        users = Object.read(b)
        
        return Blocked(blocked=blocked, users=users)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(Vector(self.blocked))
        
        b.write(Vector(self.users))
        
        return b.getvalue()
