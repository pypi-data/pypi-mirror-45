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


class SaveGif(Object):
    """Attributes:
        ID: ``0x327a30cb``

    Args:
        id: Either :obj:`InputDocumentEmpty <DevLGram.api.types.InputDocumentEmpty>` or :obj:`InputDocument <DevLGram.api.types.InputDocument>`
        unsave: ``bool``

    Raises:
        :obj:`RPCError <DevLGram.RPCError>`

    Returns:
        ``bool``
    """

    __slots__ = ["id", "unsave"]

    ID = 0x327a30cb
    QUALNAME = "messages.SaveGif"

    def __init__(self, *, id, unsave: bool):
        self.id = id  # InputDocument
        self.unsave = unsave  # Bool

    @staticmethod
    def read(b: BytesIO, *args) -> "SaveGif":
        # No flags
        
        id = Object.read(b)
        
        unsave = Bool.read(b)
        
        return SaveGif(id=id, unsave=unsave)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(self.id.write())
        
        b.write(Bool(self.unsave))
        
        return b.getvalue()
