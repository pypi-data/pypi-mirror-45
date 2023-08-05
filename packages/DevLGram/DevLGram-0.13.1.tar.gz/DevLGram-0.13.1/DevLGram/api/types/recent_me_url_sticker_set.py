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


class RecentMeUrlStickerSet(Object):
    """Attributes:
        ID: ``0xbc0a57dc``

    Args:
        url: ``str``
        set: Either :obj:`StickerSetCovered <DevLGram.api.types.StickerSetCovered>` or :obj:`StickerSetMultiCovered <DevLGram.api.types.StickerSetMultiCovered>`
    """

    __slots__ = ["url", "set"]

    ID = 0xbc0a57dc
    QUALNAME = "RecentMeUrlStickerSet"

    def __init__(self, *, url: str, set):
        self.url = url  # string
        self.set = set  # StickerSetCovered

    @staticmethod
    def read(b: BytesIO, *args) -> "RecentMeUrlStickerSet":
        # No flags
        
        url = String.read(b)
        
        set = Object.read(b)
        
        return RecentMeUrlStickerSet(url=url, set=set)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(String(self.url))
        
        b.write(self.set.write())
        
        return b.getvalue()
