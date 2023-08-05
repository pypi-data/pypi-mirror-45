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


class GetStrings(Object):
    """Attributes:
        ID: ``0xefea3803``

    Args:
        lang_pack: ``str``
        lang_code: ``str``
        keys: List of ``str``

    Raises:
        :obj:`RPCError <DevLGram.RPCError>`

    Returns:
        List of either :obj:`LangPackString <DevLGram.api.types.LangPackString>`, :obj:`LangPackStringPluralized <DevLGram.api.types.LangPackStringPluralized>` or :obj:`LangPackStringDeleted <DevLGram.api.types.LangPackStringDeleted>`
    """

    __slots__ = ["lang_pack", "lang_code", "keys"]

    ID = 0xefea3803
    QUALNAME = "langpack.GetStrings"

    def __init__(self, *, lang_pack: str, lang_code: str, keys: list):
        self.lang_pack = lang_pack  # string
        self.lang_code = lang_code  # string
        self.keys = keys  # Vector<string>

    @staticmethod
    def read(b: BytesIO, *args) -> "GetStrings":
        # No flags
        
        lang_pack = String.read(b)
        
        lang_code = String.read(b)
        
        keys = Object.read(b, String)
        
        return GetStrings(lang_pack=lang_pack, lang_code=lang_code, keys=keys)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(String(self.lang_pack))
        
        b.write(String(self.lang_code))
        
        b.write(Vector(self.keys, String))
        
        return b.getvalue()
