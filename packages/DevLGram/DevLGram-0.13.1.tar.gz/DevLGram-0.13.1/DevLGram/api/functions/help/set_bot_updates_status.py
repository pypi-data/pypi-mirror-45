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


class SetBotUpdatesStatus(Object):
    """Attributes:
        ID: ``0xec22cfcd``

    Args:
        pending_updates_count: ``int`` ``32-bit``
        message: ``str``

    Raises:
        :obj:`RPCError <DevLGram.RPCError>`

    Returns:
        ``bool``
    """

    __slots__ = ["pending_updates_count", "message"]

    ID = 0xec22cfcd
    QUALNAME = "help.SetBotUpdatesStatus"

    def __init__(self, *, pending_updates_count: int, message: str):
        self.pending_updates_count = pending_updates_count  # int
        self.message = message  # string

    @staticmethod
    def read(b: BytesIO, *args) -> "SetBotUpdatesStatus":
        # No flags
        
        pending_updates_count = Int.read(b)
        
        message = String.read(b)
        
        return SetBotUpdatesStatus(pending_updates_count=pending_updates_count, message=message)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(Int(self.pending_updates_count))
        
        b.write(String(self.message))
        
        return b.getvalue()
