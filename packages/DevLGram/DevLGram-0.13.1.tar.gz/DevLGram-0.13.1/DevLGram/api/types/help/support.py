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


class Support(Object):
    """Attributes:
        ID: ``0x17c6b5f6``

    Args:
        phone_number: ``str``
        user: Either :obj:`UserEmpty <DevLGram.api.types.UserEmpty>` or :obj:`User <DevLGram.api.types.User>`

    See Also:
        This object can be returned by :obj:`help.GetSupport <DevLGram.api.functions.help.GetSupport>`.
    """

    __slots__ = ["phone_number", "user"]

    ID = 0x17c6b5f6
    QUALNAME = "help.Support"

    def __init__(self, *, phone_number: str, user):
        self.phone_number = phone_number  # string
        self.user = user  # User

    @staticmethod
    def read(b: BytesIO, *args) -> "Support":
        # No flags
        
        phone_number = String.read(b)
        
        user = Object.read(b)
        
        return Support(phone_number=phone_number, user=user)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(String(self.phone_number))
        
        b.write(self.user.write())
        
        return b.getvalue()
