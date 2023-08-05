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


class UploadProfilePhoto(Object):
    """Attributes:
        ID: ``0x4f32c098``

    Args:
        file: Either :obj:`InputFile <DevLGram.api.types.InputFile>` or :obj:`InputFileBig <DevLGram.api.types.InputFileBig>`

    Raises:
        :obj:`RPCError <DevLGram.RPCError>`

    Returns:
        :obj:`photos.Photo <DevLGram.api.types.photos.Photo>`
    """

    __slots__ = ["file"]

    ID = 0x4f32c098
    QUALNAME = "photos.UploadProfilePhoto"

    def __init__(self, *, file):
        self.file = file  # InputFile

    @staticmethod
    def read(b: BytesIO, *args) -> "UploadProfilePhoto":
        # No flags
        
        file = Object.read(b)
        
        return UploadProfilePhoto(file=file)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(self.file.write())
        
        return b.getvalue()
