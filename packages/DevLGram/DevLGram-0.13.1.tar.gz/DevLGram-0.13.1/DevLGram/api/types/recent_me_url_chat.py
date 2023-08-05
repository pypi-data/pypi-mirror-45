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


class RecentMeUrlChat(Object):
    """Attributes:
        ID: ``0xa01b22f9``

    Args:
        url: ``str``
        chat_id: ``int`` ``32-bit``
    """

    __slots__ = ["url", "chat_id"]

    ID = 0xa01b22f9
    QUALNAME = "RecentMeUrlChat"

    def __init__(self, *, url: str, chat_id: int):
        self.url = url  # string
        self.chat_id = chat_id  # int

    @staticmethod
    def read(b: BytesIO, *args) -> "RecentMeUrlChat":
        # No flags
        
        url = String.read(b)
        
        chat_id = Int.read(b)
        
        return RecentMeUrlChat(url=url, chat_id=chat_id)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(String(self.url))
        
        b.write(Int(self.chat_id))
        
        return b.getvalue()
