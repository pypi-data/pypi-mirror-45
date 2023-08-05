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


class DeletePhotos(Object):
    """Attributes:
        ID: ``0x87cf7f2f``

    Args:
        id: List of either :obj:`InputPhotoEmpty <DevLGram.api.types.InputPhotoEmpty>` or :obj:`InputPhoto <DevLGram.api.types.InputPhoto>`

    Raises:
        :obj:`RPCError <DevLGram.RPCError>`

    Returns:
        List of ``int`` ``64-bit``
    """

    __slots__ = ["id"]

    ID = 0x87cf7f2f
    QUALNAME = "photos.DeletePhotos"

    def __init__(self, *, id: list):
        self.id = id  # Vector<InputPhoto>

    @staticmethod
    def read(b: BytesIO, *args) -> "DeletePhotos":
        # No flags
        
        id = Object.read(b)
        
        return DeletePhotos(id=id)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(Vector(self.id))
        
        return b.getvalue()
