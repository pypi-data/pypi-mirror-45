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


class GetEmojiKeywordsDifference(Object):
    """Attributes:
        ID: ``0x1508b6af``

    Args:
        lang_code: ``str``
        from_version: ``int`` ``32-bit``

    Raises:
        :obj:`RPCError <DevLGram.RPCError>`

    Returns:
        :obj:`EmojiKeywordsDifference <DevLGram.api.types.EmojiKeywordsDifference>`
    """

    __slots__ = ["lang_code", "from_version"]

    ID = 0x1508b6af
    QUALNAME = "messages.GetEmojiKeywordsDifference"

    def __init__(self, *, lang_code: str, from_version: int):
        self.lang_code = lang_code  # string
        self.from_version = from_version  # int

    @staticmethod
    def read(b: BytesIO, *args) -> "GetEmojiKeywordsDifference":
        # No flags
        
        lang_code = String.read(b)
        
        from_version = Int.read(b)
        
        return GetEmojiKeywordsDifference(lang_code=lang_code, from_version=from_version)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(String(self.lang_code))
        
        b.write(Int(self.from_version))
        
        return b.getvalue()
