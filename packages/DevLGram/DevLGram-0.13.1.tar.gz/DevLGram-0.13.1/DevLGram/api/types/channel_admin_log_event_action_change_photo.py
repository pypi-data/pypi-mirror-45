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


class ChannelAdminLogEventActionChangePhoto(Object):
    """Attributes:
        ID: ``0xb82f55c3``

    Args:
        prev_photo: Either :obj:`ChatPhotoEmpty <DevLGram.api.types.ChatPhotoEmpty>` or :obj:`ChatPhoto <DevLGram.api.types.ChatPhoto>`
        new_photo: Either :obj:`ChatPhotoEmpty <DevLGram.api.types.ChatPhotoEmpty>` or :obj:`ChatPhoto <DevLGram.api.types.ChatPhoto>`
    """

    __slots__ = ["prev_photo", "new_photo"]

    ID = 0xb82f55c3
    QUALNAME = "ChannelAdminLogEventActionChangePhoto"

    def __init__(self, *, prev_photo, new_photo):
        self.prev_photo = prev_photo  # ChatPhoto
        self.new_photo = new_photo  # ChatPhoto

    @staticmethod
    def read(b: BytesIO, *args) -> "ChannelAdminLogEventActionChangePhoto":
        # No flags
        
        prev_photo = Object.read(b)
        
        new_photo = Object.read(b)
        
        return ChannelAdminLogEventActionChangePhoto(prev_photo=prev_photo, new_photo=new_photo)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(self.prev_photo.write())
        
        b.write(self.new_photo.write())
        
        return b.getvalue()
