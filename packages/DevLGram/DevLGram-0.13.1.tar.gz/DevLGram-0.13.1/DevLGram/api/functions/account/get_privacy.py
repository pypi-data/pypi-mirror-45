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


class GetPrivacy(Object):
    """Attributes:
        ID: ``0xdadbc950``

    Args:
        key: Either :obj:`InputPrivacyKeyStatusTimestamp <DevLGram.api.types.InputPrivacyKeyStatusTimestamp>`, :obj:`InputPrivacyKeyChatInvite <DevLGram.api.types.InputPrivacyKeyChatInvite>`, :obj:`InputPrivacyKeyPhoneCall <DevLGram.api.types.InputPrivacyKeyPhoneCall>`, :obj:`InputPrivacyKeyPhoneP2P <DevLGram.api.types.InputPrivacyKeyPhoneP2P>`, :obj:`InputPrivacyKeyForwards <DevLGram.api.types.InputPrivacyKeyForwards>` or :obj:`InputPrivacyKeyProfilePhoto <DevLGram.api.types.InputPrivacyKeyProfilePhoto>`

    Raises:
        :obj:`RPCError <DevLGram.RPCError>`

    Returns:
        :obj:`account.PrivacyRules <DevLGram.api.types.account.PrivacyRules>`
    """

    __slots__ = ["key"]

    ID = 0xdadbc950
    QUALNAME = "account.GetPrivacy"

    def __init__(self, *, key):
        self.key = key  # InputPrivacyKey

    @staticmethod
    def read(b: BytesIO, *args) -> "GetPrivacy":
        # No flags
        
        key = Object.read(b)
        
        return GetPrivacy(key=key)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(self.key.write())
        
        return b.getvalue()
