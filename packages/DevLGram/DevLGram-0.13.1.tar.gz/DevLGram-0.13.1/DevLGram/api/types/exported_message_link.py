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


class ExportedMessageLink(Object):
    """Attributes:
        ID: ``0x5dab1af4``

    Args:
        link: ``str``
        html: ``str``

    See Also:
        This object can be returned by :obj:`channels.ExportMessageLink <DevLGram.api.functions.channels.ExportMessageLink>`.
    """

    __slots__ = ["link", "html"]

    ID = 0x5dab1af4
    QUALNAME = "ExportedMessageLink"

    def __init__(self, *, link: str, html: str):
        self.link = link  # string
        self.html = html  # string

    @staticmethod
    def read(b: BytesIO, *args) -> "ExportedMessageLink":
        # No flags
        
        link = String.read(b)
        
        html = String.read(b)
        
        return ExportedMessageLink(link=link, html=html)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(String(self.link))
        
        b.write(String(self.html))
        
        return b.getvalue()
