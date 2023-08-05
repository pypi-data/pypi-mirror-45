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
        ID: ``0x63c66506``

    Args:
        id: List of either :obj:`InputMessageID <DevLGram.api.types.InputMessageID>`, :obj:`InputMessageReplyTo <DevLGram.api.types.InputMessageReplyTo>` or :obj:`InputMessagePinned <DevLGram.api.types.InputMessagePinned>`

    Raises:
        :obj:`RPCError <DevLGram.RPCError>`

    Returns:
        Either :obj:`messages.Messages <DevLGram.api.types.messages.Messages>`, :obj:`messages.MessagesSlice <DevLGram.api.types.messages.MessagesSlice>`, :obj:`messages.ChannelMessages <DevLGram.api.types.messages.ChannelMessages>` or :obj:`messages.MessagesNotModified <DevLGram.api.types.messages.MessagesNotModified>`
    """

    __slots__ = ["id"]

    ID = 0x63c66506
    QUALNAME = "messages.GetMessages"

    def __init__(self, *, id: list):
        self.id = id  # Vector<InputMessage>

    @staticmethod
    def read(b: BytesIO, *args) -> "GetMessages":
        # No flags
        
        id = Object.read(b)
        
        return GetMessages(id=id)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(Vector(self.id))
        
        return b.getvalue()
