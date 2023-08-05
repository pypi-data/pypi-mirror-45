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


class GetMessages(Object):
    """Attributes:
        ID: ``0xad8c9a23``

    Args:
        channel: Either :obj:`InputChannelEmpty <DevLGram.api.types.InputChannelEmpty>` or :obj:`InputChannel <DevLGram.api.types.InputChannel>`
        id: List of either :obj:`InputMessageID <DevLGram.api.types.InputMessageID>`, :obj:`InputMessageReplyTo <DevLGram.api.types.InputMessageReplyTo>` or :obj:`InputMessagePinned <DevLGram.api.types.InputMessagePinned>`

    Raises:
        :obj:`RPCError <DevLGram.RPCError>`

    Returns:
        Either :obj:`messages.Messages <DevLGram.api.types.messages.Messages>`, :obj:`messages.MessagesSlice <DevLGram.api.types.messages.MessagesSlice>`, :obj:`messages.ChannelMessages <DevLGram.api.types.messages.ChannelMessages>` or :obj:`messages.MessagesNotModified <DevLGram.api.types.messages.MessagesNotModified>`
    """

    __slots__ = ["channel", "id"]

    ID = 0xad8c9a23
    QUALNAME = "channels.GetMessages"

    def __init__(self, *, channel, id: list):
        self.channel = channel  # InputChannel
        self.id = id  # Vector<InputMessage>

    @staticmethod
    def read(b: BytesIO, *args) -> "GetMessages":
        # No flags
        
        channel = Object.read(b)
        
        id = Object.read(b)
        
        return GetMessages(channel=channel, id=id)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(self.channel.write())
        
        b.write(Vector(self.id))
        
        return b.getvalue()
