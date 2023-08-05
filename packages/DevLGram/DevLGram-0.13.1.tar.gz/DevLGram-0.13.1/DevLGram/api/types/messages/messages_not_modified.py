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


class MessagesNotModified(Object):
    """Attributes:
        ID: ``0x74535f21``

    Args:
        count: ``int`` ``32-bit``

    See Also:
        This object can be returned by :obj:`messages.GetMessages <DevLGram.api.functions.messages.GetMessages>`, :obj:`messages.GetHistory <DevLGram.api.functions.messages.GetHistory>`, :obj:`messages.Search <DevLGram.api.functions.messages.Search>`, :obj:`messages.SearchGlobal <DevLGram.api.functions.messages.SearchGlobal>`, :obj:`messages.GetUnreadMentions <DevLGram.api.functions.messages.GetUnreadMentions>`, :obj:`messages.GetRecentLocations <DevLGram.api.functions.messages.GetRecentLocations>` and :obj:`channels.GetMessages <DevLGram.api.functions.channels.GetMessages>`.
    """

    __slots__ = ["count"]

    ID = 0x74535f21
    QUALNAME = "messages.MessagesNotModified"

    def __init__(self, *, count: int):
        self.count = count  # int

    @staticmethod
    def read(b: BytesIO, *args) -> "MessagesNotModified":
        # No flags
        
        count = Int.read(b)
        
        return MessagesNotModified(count=count)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(Int(self.count))
        
        return b.getvalue()
