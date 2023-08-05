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


class WebAuthorizations(Object):
    """Attributes:
        ID: ``0xed56c9fc``

    Args:
        authorizations: List of :obj:`WebAuthorization <DevLGram.api.types.WebAuthorization>`
        users: List of either :obj:`UserEmpty <DevLGram.api.types.UserEmpty>` or :obj:`User <DevLGram.api.types.User>`

    See Also:
        This object can be returned by :obj:`account.GetWebAuthorizations <DevLGram.api.functions.account.GetWebAuthorizations>`.
    """

    __slots__ = ["authorizations", "users"]

    ID = 0xed56c9fc
    QUALNAME = "account.WebAuthorizations"

    def __init__(self, *, authorizations: list, users: list):
        self.authorizations = authorizations  # Vector<WebAuthorization>
        self.users = users  # Vector<User>

    @staticmethod
    def read(b: BytesIO, *args) -> "WebAuthorizations":
        # No flags
        
        authorizations = Object.read(b)
        
        users = Object.read(b)
        
        return WebAuthorizations(authorizations=authorizations, users=users)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(Vector(self.authorizations))
        
        b.write(Vector(self.users))
        
        return b.getvalue()
