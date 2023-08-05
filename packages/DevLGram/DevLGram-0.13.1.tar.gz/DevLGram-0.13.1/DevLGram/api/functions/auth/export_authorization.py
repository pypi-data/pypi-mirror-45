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


class ExportAuthorization(Object):
    """Attributes:
        ID: ``0xe5bfffcd``

    Args:
        dc_id: ``int`` ``32-bit``

    Raises:
        :obj:`RPCError <DevLGram.RPCError>`

    Returns:
        :obj:`auth.ExportedAuthorization <DevLGram.api.types.auth.ExportedAuthorization>`
    """

    __slots__ = ["dc_id"]

    ID = 0xe5bfffcd
    QUALNAME = "auth.ExportAuthorization"

    def __init__(self, *, dc_id: int):
        self.dc_id = dc_id  # int

    @staticmethod
    def read(b: BytesIO, *args) -> "ExportAuthorization":
        # No flags
        
        dc_id = Int.read(b)
        
        return ExportAuthorization(dc_id=dc_id)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(Int(self.dc_id))
        
        return b.getvalue()
