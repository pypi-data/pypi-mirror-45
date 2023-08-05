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


class PrivacyRules(Object):
    """Attributes:
        ID: ``0x554abb6f``

    Args:
        rules: List of either :obj:`PrivacyValueAllowContacts <DevLGram.api.types.PrivacyValueAllowContacts>`, :obj:`PrivacyValueAllowAll <DevLGram.api.types.PrivacyValueAllowAll>`, :obj:`PrivacyValueAllowUsers <DevLGram.api.types.PrivacyValueAllowUsers>`, :obj:`PrivacyValueDisallowContacts <DevLGram.api.types.PrivacyValueDisallowContacts>`, :obj:`PrivacyValueDisallowAll <DevLGram.api.types.PrivacyValueDisallowAll>` or :obj:`PrivacyValueDisallowUsers <DevLGram.api.types.PrivacyValueDisallowUsers>`
        users: List of either :obj:`UserEmpty <DevLGram.api.types.UserEmpty>` or :obj:`User <DevLGram.api.types.User>`

    See Also:
        This object can be returned by :obj:`account.GetPrivacy <DevLGram.api.functions.account.GetPrivacy>` and :obj:`account.SetPrivacy <DevLGram.api.functions.account.SetPrivacy>`.
    """

    __slots__ = ["rules", "users"]

    ID = 0x554abb6f
    QUALNAME = "account.PrivacyRules"

    def __init__(self, *, rules: list, users: list):
        self.rules = rules  # Vector<PrivacyRule>
        self.users = users  # Vector<User>

    @staticmethod
    def read(b: BytesIO, *args) -> "PrivacyRules":
        # No flags
        
        rules = Object.read(b)
        
        users = Object.read(b)
        
        return PrivacyRules(rules=rules, users=users)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(Vector(self.rules))
        
        b.write(Vector(self.users))
        
        return b.getvalue()
