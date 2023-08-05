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


class EmojiKeywordsDifference(Object):
    """Attributes:
        ID: ``0x5cc761bd``

    Args:
        lang_code: ``str``
        from_version: ``int`` ``32-bit``
        version: ``int`` ``32-bit``
        keywords: List of either :obj:`EmojiKeyword <DevLGram.api.types.EmojiKeyword>` or :obj:`EmojiKeywordDeleted <DevLGram.api.types.EmojiKeywordDeleted>`

    See Also:
        This object can be returned by :obj:`messages.GetEmojiKeywords <DevLGram.api.functions.messages.GetEmojiKeywords>` and :obj:`messages.GetEmojiKeywordsDifference <DevLGram.api.functions.messages.GetEmojiKeywordsDifference>`.
    """

    __slots__ = ["lang_code", "from_version", "version", "keywords"]

    ID = 0x5cc761bd
    QUALNAME = "EmojiKeywordsDifference"

    def __init__(self, *, lang_code: str, from_version: int, version: int, keywords: list):
        self.lang_code = lang_code  # string
        self.from_version = from_version  # int
        self.version = version  # int
        self.keywords = keywords  # Vector<EmojiKeyword>

    @staticmethod
    def read(b: BytesIO, *args) -> "EmojiKeywordsDifference":
        # No flags
        
        lang_code = String.read(b)
        
        from_version = Int.read(b)
        
        version = Int.read(b)
        
        keywords = Object.read(b)
        
        return EmojiKeywordsDifference(lang_code=lang_code, from_version=from_version, version=version, keywords=keywords)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(String(self.lang_code))
        
        b.write(Int(self.from_version))
        
        b.write(Int(self.version))
        
        b.write(Vector(self.keywords))
        
        return b.getvalue()
