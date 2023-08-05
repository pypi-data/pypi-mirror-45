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


class KeyboardButtonCallback(Object):
    """Attributes:
        ID: ``0x683a5e46``

    Args:
        text: ``str``
        data: ``bytes``
    """

    __slots__ = ["text", "data"]

    ID = 0x683a5e46
    QUALNAME = "KeyboardButtonCallback"

    def __init__(self, *, text: str, data: bytes):
        self.text = text  # string
        self.data = data  # bytes

    @staticmethod
    def read(b: BytesIO, *args) -> "KeyboardButtonCallback":
        # No flags
        
        text = String.read(b)
        
        data = Bytes.read(b)
        
        return KeyboardButtonCallback(text=text, data=data)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(String(self.text))
        
        b.write(Bytes(self.data))
        
        return b.getvalue()
