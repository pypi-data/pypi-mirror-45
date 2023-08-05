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


class ContactStatus(Object):
    """Attributes:
        ID: ``0xd3680c61``

    Args:
        user_id: ``int`` ``32-bit``
        status: Either :obj:`UserStatusEmpty <DevLGram.api.types.UserStatusEmpty>`, :obj:`UserStatusOnline <DevLGram.api.types.UserStatusOnline>`, :obj:`UserStatusOffline <DevLGram.api.types.UserStatusOffline>`, :obj:`UserStatusRecently <DevLGram.api.types.UserStatusRecently>`, :obj:`UserStatusLastWeek <DevLGram.api.types.UserStatusLastWeek>` or :obj:`UserStatusLastMonth <DevLGram.api.types.UserStatusLastMonth>`

    See Also:
        This object can be returned by :obj:`contacts.GetStatuses <DevLGram.api.functions.contacts.GetStatuses>`.
    """

    __slots__ = ["user_id", "status"]

    ID = 0xd3680c61
    QUALNAME = "ContactStatus"

    def __init__(self, *, user_id: int, status):
        self.user_id = user_id  # int
        self.status = status  # UserStatus

    @staticmethod
    def read(b: BytesIO, *args) -> "ContactStatus":
        # No flags
        
        user_id = Int.read(b)
        
        status = Object.read(b)
        
        return ContactStatus(user_id=user_id, status=status)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(Int(self.user_id))
        
        b.write(self.status.write())
        
        return b.getvalue()
