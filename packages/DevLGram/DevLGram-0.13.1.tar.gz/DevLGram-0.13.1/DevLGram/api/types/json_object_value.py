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


class JsonObjectValue(Object):
    """Attributes:
        ID: ``0xc0de1bd9``

    Args:
        key: ``str``
        value: Either :obj:`JsonNull <DevLGram.api.types.JsonNull>`, :obj:`JsonBool <DevLGram.api.types.JsonBool>`, :obj:`JsonNumber <DevLGram.api.types.JsonNumber>`, :obj:`JsonString <DevLGram.api.types.JsonString>`, :obj:`JsonArray <DevLGram.api.types.JsonArray>` or :obj:`JsonObject <DevLGram.api.types.JsonObject>`
    """

    __slots__ = ["key", "value"]

    ID = 0xc0de1bd9
    QUALNAME = "JsonObjectValue"

    def __init__(self, *, key: str, value):
        self.key = key  # string
        self.value = value  # JSONValue

    @staticmethod
    def read(b: BytesIO, *args) -> "JsonObjectValue":
        # No flags
        
        key = String.read(b)
        
        value = Object.read(b)
        
        return JsonObjectValue(key=key, value=value)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(String(self.key))
        
        b.write(self.value.write())
        
        return b.getvalue()
