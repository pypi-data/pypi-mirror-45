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


class GetDeepLinkInfo(Object):
    """Attributes:
        ID: ``0x3fedc75f``

    Args:
        path: ``str``

    Raises:
        :obj:`RPCError <DevLGram.RPCError>`

    Returns:
        Either :obj:`help.DeepLinkInfoEmpty <DevLGram.api.types.help.DeepLinkInfoEmpty>` or :obj:`help.DeepLinkInfo <DevLGram.api.types.help.DeepLinkInfo>`
    """

    __slots__ = ["path"]

    ID = 0x3fedc75f
    QUALNAME = "help.GetDeepLinkInfo"

    def __init__(self, *, path: str):
        self.path = path  # string

    @staticmethod
    def read(b: BytesIO, *args) -> "GetDeepLinkInfo":
        # No flags
        
        path = String.read(b)
        
        return GetDeepLinkInfo(path=path)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(String(self.path))
        
        return b.getvalue()
