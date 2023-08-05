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


class SetPrivacy(Object):
    """Attributes:
        ID: ``0xc9f81ce8``

    Args:
        key: Either :obj:`InputPrivacyKeyStatusTimestamp <DevLGram.api.types.InputPrivacyKeyStatusTimestamp>`, :obj:`InputPrivacyKeyChatInvite <DevLGram.api.types.InputPrivacyKeyChatInvite>`, :obj:`InputPrivacyKeyPhoneCall <DevLGram.api.types.InputPrivacyKeyPhoneCall>`, :obj:`InputPrivacyKeyPhoneP2P <DevLGram.api.types.InputPrivacyKeyPhoneP2P>`, :obj:`InputPrivacyKeyForwards <DevLGram.api.types.InputPrivacyKeyForwards>` or :obj:`InputPrivacyKeyProfilePhoto <DevLGram.api.types.InputPrivacyKeyProfilePhoto>`
        rules: List of either :obj:`InputPrivacyValueAllowContacts <DevLGram.api.types.InputPrivacyValueAllowContacts>`, :obj:`InputPrivacyValueAllowAll <DevLGram.api.types.InputPrivacyValueAllowAll>`, :obj:`InputPrivacyValueAllowUsers <DevLGram.api.types.InputPrivacyValueAllowUsers>`, :obj:`InputPrivacyValueDisallowContacts <DevLGram.api.types.InputPrivacyValueDisallowContacts>`, :obj:`InputPrivacyValueDisallowAll <DevLGram.api.types.InputPrivacyValueDisallowAll>` or :obj:`InputPrivacyValueDisallowUsers <DevLGram.api.types.InputPrivacyValueDisallowUsers>`

    Raises:
        :obj:`RPCError <DevLGram.RPCError>`

    Returns:
        :obj:`account.PrivacyRules <DevLGram.api.types.account.PrivacyRules>`
    """

    __slots__ = ["key", "rules"]

    ID = 0xc9f81ce8
    QUALNAME = "account.SetPrivacy"

    def __init__(self, *, key, rules: list):
        self.key = key  # InputPrivacyKey
        self.rules = rules  # Vector<InputPrivacyRule>

    @staticmethod
    def read(b: BytesIO, *args) -> "SetPrivacy":
        # No flags
        
        key = Object.read(b)
        
        rules = Object.read(b)
        
        return SetPrivacy(key=key, rules=rules)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(self.key.write())
        
        b.write(Vector(self.rules))
        
        return b.getvalue()
