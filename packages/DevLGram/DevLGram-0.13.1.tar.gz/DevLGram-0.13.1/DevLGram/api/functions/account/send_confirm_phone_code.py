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


class SendConfirmPhoneCode(Object):
    """Attributes:
        ID: ``0x1b3faa88``

    Args:
        hash: ``str``
        settings: :obj:`CodeSettings <DevLGram.api.types.CodeSettings>`

    Raises:
        :obj:`RPCError <DevLGram.RPCError>`

    Returns:
        :obj:`auth.SentCode <DevLGram.api.types.auth.SentCode>`
    """

    __slots__ = ["hash", "settings"]

    ID = 0x1b3faa88
    QUALNAME = "account.SendConfirmPhoneCode"

    def __init__(self, *, hash: str, settings):
        self.hash = hash  # string
        self.settings = settings  # CodeSettings

    @staticmethod
    def read(b: BytesIO, *args) -> "SendConfirmPhoneCode":
        # No flags
        
        hash = String.read(b)
        
        settings = Object.read(b)
        
        return SendConfirmPhoneCode(hash=hash, settings=settings)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(String(self.hash))
        
        b.write(self.settings.write())
        
        return b.getvalue()
