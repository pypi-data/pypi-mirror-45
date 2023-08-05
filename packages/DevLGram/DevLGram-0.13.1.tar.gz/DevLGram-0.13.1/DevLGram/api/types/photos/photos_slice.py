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


class PhotosSlice(Object):
    """Attributes:
        ID: ``0x15051f54``

    Args:
        count: ``int`` ``32-bit``
        photos: List of either :obj:`PhotoEmpty <DevLGram.api.types.PhotoEmpty>` or :obj:`Photo <DevLGram.api.types.Photo>`
        users: List of either :obj:`UserEmpty <DevLGram.api.types.UserEmpty>` or :obj:`User <DevLGram.api.types.User>`

    See Also:
        This object can be returned by :obj:`photos.GetUserPhotos <DevLGram.api.functions.photos.GetUserPhotos>`.
    """

    __slots__ = ["count", "photos", "users"]

    ID = 0x15051f54
    QUALNAME = "photos.PhotosSlice"

    def __init__(self, *, count: int, photos: list, users: list):
        self.count = count  # int
        self.photos = photos  # Vector<Photo>
        self.users = users  # Vector<User>

    @staticmethod
    def read(b: BytesIO, *args) -> "PhotosSlice":
        # No flags
        
        count = Int.read(b)
        
        photos = Object.read(b)
        
        users = Object.read(b)
        
        return PhotosSlice(count=count, photos=photos, users=users)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(Int(self.count))
        
        b.write(Vector(self.photos))
        
        b.write(Vector(self.users))
        
        return b.getvalue()
