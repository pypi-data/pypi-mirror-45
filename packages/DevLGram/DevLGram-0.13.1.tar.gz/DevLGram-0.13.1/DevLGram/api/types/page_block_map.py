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


class PageBlockMap(Object):
    """Attributes:
        ID: ``0xa44f3ef6``

    Args:
        geo: Either :obj:`GeoPointEmpty <DevLGram.api.types.GeoPointEmpty>` or :obj:`GeoPoint <DevLGram.api.types.GeoPoint>`
        zoom: ``int`` ``32-bit``
        w: ``int`` ``32-bit``
        h: ``int`` ``32-bit``
        caption: :obj:`PageCaption <DevLGram.api.types.PageCaption>`
    """

    __slots__ = ["geo", "zoom", "w", "h", "caption"]

    ID = 0xa44f3ef6
    QUALNAME = "PageBlockMap"

    def __init__(self, *, geo, zoom: int, w: int, h: int, caption):
        self.geo = geo  # GeoPoint
        self.zoom = zoom  # int
        self.w = w  # int
        self.h = h  # int
        self.caption = caption  # PageCaption

    @staticmethod
    def read(b: BytesIO, *args) -> "PageBlockMap":
        # No flags
        
        geo = Object.read(b)
        
        zoom = Int.read(b)
        
        w = Int.read(b)
        
        h = Int.read(b)
        
        caption = Object.read(b)
        
        return PageBlockMap(geo=geo, zoom=zoom, w=w, h=h, caption=caption)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(self.geo.write())
        
        b.write(Int(self.zoom))
        
        b.write(Int(self.w))
        
        b.write(Int(self.h))
        
        b.write(self.caption.write())
        
        return b.getvalue()
