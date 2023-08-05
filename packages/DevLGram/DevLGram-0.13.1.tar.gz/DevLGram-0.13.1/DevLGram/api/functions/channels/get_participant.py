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


class GetParticipant(Object):
    """Attributes:
        ID: ``0x546dd7a6``

    Args:
        channel: Either :obj:`InputChannelEmpty <DevLGram.api.types.InputChannelEmpty>` or :obj:`InputChannel <DevLGram.api.types.InputChannel>`
        user_id: Either :obj:`InputUserEmpty <DevLGram.api.types.InputUserEmpty>`, :obj:`InputUserSelf <DevLGram.api.types.InputUserSelf>` or :obj:`InputUser <DevLGram.api.types.InputUser>`

    Raises:
        :obj:`RPCError <DevLGram.RPCError>`

    Returns:
        :obj:`channels.ChannelParticipant <DevLGram.api.types.channels.ChannelParticipant>`
    """

    __slots__ = ["channel", "user_id"]

    ID = 0x546dd7a6
    QUALNAME = "channels.GetParticipant"

    def __init__(self, *, channel, user_id):
        self.channel = channel  # InputChannel
        self.user_id = user_id  # InputUser

    @staticmethod
    def read(b: BytesIO, *args) -> "GetParticipant":
        # No flags
        
        channel = Object.read(b)
        
        user_id = Object.read(b)
        
        return GetParticipant(channel=channel, user_id=user_id)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(self.channel.write())
        
        b.write(self.user_id.write())
        
        return b.getvalue()
