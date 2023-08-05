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


class GetWebPage(Object):
    """Attributes:
        ID: ``0x32ca8f91``

    Args:
        url: ``str``
        hash: ``int`` ``32-bit``

    Raises:
        :obj:`RPCError <DevLGram.RPCError>`

    Returns:
        Either :obj:`WebPageEmpty <DevLGram.api.types.WebPageEmpty>`, :obj:`WebPagePending <DevLGram.api.types.WebPagePending>`, :obj:`WebPage <DevLGram.api.types.WebPage>` or :obj:`WebPageNotModified <DevLGram.api.types.WebPageNotModified>`
    """

    __slots__ = ["url", "hash"]

    ID = 0x32ca8f91
    QUALNAME = "messages.GetWebPage"

    def __init__(self, *, url: str, hash: int):
        self.url = url  # string
        self.hash = hash  # int

    @staticmethod
    def read(b: BytesIO, *args) -> "GetWebPage":
        # No flags
        
        url = String.read(b)
        
        hash = Int.read(b)
        
        return GetWebPage(url=url, hash=hash)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(String(self.url))
        
        b.write(Int(self.hash))
        
        return b.getvalue()
