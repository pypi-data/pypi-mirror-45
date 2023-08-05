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


class UpdatePrivacy(Object):
    """Attributes:
        ID: ``0xee3b272a``

    Args:
        key: Either :obj:`PrivacyKeyStatusTimestamp <DevLGram.api.types.PrivacyKeyStatusTimestamp>`, :obj:`PrivacyKeyChatInvite <DevLGram.api.types.PrivacyKeyChatInvite>`, :obj:`PrivacyKeyPhoneCall <DevLGram.api.types.PrivacyKeyPhoneCall>`, :obj:`PrivacyKeyPhoneP2P <DevLGram.api.types.PrivacyKeyPhoneP2P>`, :obj:`PrivacyKeyForwards <DevLGram.api.types.PrivacyKeyForwards>` or :obj:`PrivacyKeyProfilePhoto <DevLGram.api.types.PrivacyKeyProfilePhoto>`
        rules: List of either :obj:`PrivacyValueAllowContacts <DevLGram.api.types.PrivacyValueAllowContacts>`, :obj:`PrivacyValueAllowAll <DevLGram.api.types.PrivacyValueAllowAll>`, :obj:`PrivacyValueAllowUsers <DevLGram.api.types.PrivacyValueAllowUsers>`, :obj:`PrivacyValueDisallowContacts <DevLGram.api.types.PrivacyValueDisallowContacts>`, :obj:`PrivacyValueDisallowAll <DevLGram.api.types.PrivacyValueDisallowAll>` or :obj:`PrivacyValueDisallowUsers <DevLGram.api.types.PrivacyValueDisallowUsers>`
    """

    __slots__ = ["key", "rules"]

    ID = 0xee3b272a
    QUALNAME = "UpdatePrivacy"

    def __init__(self, *, key, rules: list):
        self.key = key  # PrivacyKey
        self.rules = rules  # Vector<PrivacyRule>

    @staticmethod
    def read(b: BytesIO, *args) -> "UpdatePrivacy":
        # No flags
        
        key = Object.read(b)
        
        rules = Object.read(b)
        
        return UpdatePrivacy(key=key, rules=rules)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(self.key.write())
        
        b.write(Vector(self.rules))
        
        return b.getvalue()
