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


class JsonArray(Object):
    """Attributes:
        ID: ``0xf7444763``

    Args:
        value: List of either :obj:`JsonNull <DevLGram.api.types.JsonNull>`, :obj:`JsonBool <DevLGram.api.types.JsonBool>`, :obj:`JsonNumber <DevLGram.api.types.JsonNumber>`, :obj:`JsonString <DevLGram.api.types.JsonString>`, :obj:`JsonArray <DevLGram.api.types.JsonArray>` or :obj:`JsonObject <DevLGram.api.types.JsonObject>`

    See Also:
        This object can be returned by :obj:`help.GetAppConfig <DevLGram.api.functions.help.GetAppConfig>`.
    """

    __slots__ = ["value"]

    ID = 0xf7444763
    QUALNAME = "JsonArray"

    def __init__(self, *, value: list):
        self.value = value  # Vector<JSONValue>

    @staticmethod
    def read(b: BytesIO, *args) -> "JsonArray":
        # No flags
        
        value = Object.read(b)
        
        return JsonArray(value=value)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(Vector(self.value))
        
        return b.getvalue()
