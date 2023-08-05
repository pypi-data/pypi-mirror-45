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


class GetAppUpdate(Object):
    """Attributes:
        ID: ``0x522d5a7d``

    Args:
        source: ``str``

    Raises:
        :obj:`RPCError <DevLGram.RPCError>`

    Returns:
        Either :obj:`help.AppUpdate <DevLGram.api.types.help.AppUpdate>` or :obj:`help.NoAppUpdate <DevLGram.api.types.help.NoAppUpdate>`
    """

    __slots__ = ["source"]

    ID = 0x522d5a7d
    QUALNAME = "help.GetAppUpdate"

    def __init__(self, *, source: str):
        self.source = source  # string

    @staticmethod
    def read(b: BytesIO, *args) -> "GetAppUpdate":
        # No flags
        
        source = String.read(b)
        
        return GetAppUpdate(source=source)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(String(self.source))
        
        return b.getvalue()
