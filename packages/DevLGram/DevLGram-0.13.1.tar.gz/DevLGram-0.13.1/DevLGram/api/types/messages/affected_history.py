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


class AffectedHistory(Object):
    """Attributes:
        ID: ``0xb45c69d1``

    Args:
        pts: ``int`` ``32-bit``
        pts_count: ``int`` ``32-bit``
        offset: ``int`` ``32-bit``

    See Also:
        This object can be returned by :obj:`messages.DeleteHistory <DevLGram.api.functions.messages.DeleteHistory>`, :obj:`messages.ReadMentions <DevLGram.api.functions.messages.ReadMentions>` and :obj:`channels.DeleteUserHistory <DevLGram.api.functions.channels.DeleteUserHistory>`.
    """

    __slots__ = ["pts", "pts_count", "offset"]

    ID = 0xb45c69d1
    QUALNAME = "messages.AffectedHistory"

    def __init__(self, *, pts: int, pts_count: int, offset: int):
        self.pts = pts  # int
        self.pts_count = pts_count  # int
        self.offset = offset  # int

    @staticmethod
    def read(b: BytesIO, *args) -> "AffectedHistory":
        # No flags
        
        pts = Int.read(b)
        
        pts_count = Int.read(b)
        
        offset = Int.read(b)
        
        return AffectedHistory(pts=pts, pts_count=pts_count, offset=offset)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(Int(self.pts))
        
        b.write(Int(self.pts_count))
        
        b.write(Int(self.offset))
        
        return b.getvalue()
