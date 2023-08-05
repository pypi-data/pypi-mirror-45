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


class DestroySessionNone(Object):
    """Attributes:
        ID: ``0x62d350c9``

    Args:
        session_id: ``int`` ``64-bit``

    See Also:
        This object can be returned by :obj:`DestroySession <DevLGram.api.functions.DestroySession>`.
    """

    __slots__ = ["session_id"]

    ID = 0x62d350c9
    QUALNAME = "DestroySessionNone"

    def __init__(self, *, session_id: int):
        self.session_id = session_id  # long

    @staticmethod
    def read(b: BytesIO, *args) -> "DestroySessionNone":
        # No flags
        
        session_id = Long.read(b)
        
        return DestroySessionNone(session_id=session_id)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(Long(self.session_id))
        
        return b.getvalue()
