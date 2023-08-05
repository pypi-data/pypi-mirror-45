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


class GetLanguage(Object):
    """Attributes:
        ID: ``0x6a596502``

    Args:
        lang_pack: ``str``
        lang_code: ``str``

    Raises:
        :obj:`RPCError <DevLGram.RPCError>`

    Returns:
        :obj:`LangPackLanguage <DevLGram.api.types.LangPackLanguage>`
    """

    __slots__ = ["lang_pack", "lang_code"]

    ID = 0x6a596502
    QUALNAME = "langpack.GetLanguage"

    def __init__(self, *, lang_pack: str, lang_code: str):
        self.lang_pack = lang_pack  # string
        self.lang_code = lang_code  # string

    @staticmethod
    def read(b: BytesIO, *args) -> "GetLanguage":
        # No flags
        
        lang_pack = String.read(b)
        
        lang_code = String.read(b)
        
        return GetLanguage(lang_pack=lang_pack, lang_code=lang_code)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(String(self.lang_pack))
        
        b.write(String(self.lang_code))
        
        return b.getvalue()
