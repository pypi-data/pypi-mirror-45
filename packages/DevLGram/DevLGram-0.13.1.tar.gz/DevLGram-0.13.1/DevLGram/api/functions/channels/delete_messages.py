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


class DeleteMessages(Object):
    """Attributes:
        ID: ``0x84c1fd4e``

    Args:
        channel: Either :obj:`InputChannelEmpty <DevLGram.api.types.InputChannelEmpty>` or :obj:`InputChannel <DevLGram.api.types.InputChannel>`
        id: List of ``int`` ``32-bit``

    Raises:
        :obj:`RPCError <DevLGram.RPCError>`

    Returns:
        :obj:`messages.AffectedMessages <DevLGram.api.types.messages.AffectedMessages>`
    """

    __slots__ = ["channel", "id"]

    ID = 0x84c1fd4e
    QUALNAME = "channels.DeleteMessages"

    def __init__(self, *, channel, id: list):
        self.channel = channel  # InputChannel
        self.id = id  # Vector<int>

    @staticmethod
    def read(b: BytesIO, *args) -> "DeleteMessages":
        # No flags
        
        channel = Object.read(b)
        
        id = Object.read(b, Int)
        
        return DeleteMessages(channel=channel, id=id)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(self.channel.write())
        
        b.write(Vector(self.id, Int))
        
        return b.getvalue()
