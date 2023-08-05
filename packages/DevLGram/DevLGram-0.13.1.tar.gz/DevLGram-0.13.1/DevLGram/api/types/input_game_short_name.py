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


class InputGameShortName(Object):
    """Attributes:
        ID: ``0xc331e80a``

    Args:
        bot_id: Either :obj:`InputUserEmpty <DevLGram.api.types.InputUserEmpty>`, :obj:`InputUserSelf <DevLGram.api.types.InputUserSelf>` or :obj:`InputUser <DevLGram.api.types.InputUser>`
        short_name: ``str``
    """

    __slots__ = ["bot_id", "short_name"]

    ID = 0xc331e80a
    QUALNAME = "InputGameShortName"

    def __init__(self, *, bot_id, short_name: str):
        self.bot_id = bot_id  # InputUser
        self.short_name = short_name  # string

    @staticmethod
    def read(b: BytesIO, *args) -> "InputGameShortName":
        # No flags
        
        bot_id = Object.read(b)
        
        short_name = String.read(b)
        
        return InputGameShortName(bot_id=bot_id, short_name=short_name)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(self.bot_id.write())
        
        b.write(String(self.short_name))
        
        return b.getvalue()
