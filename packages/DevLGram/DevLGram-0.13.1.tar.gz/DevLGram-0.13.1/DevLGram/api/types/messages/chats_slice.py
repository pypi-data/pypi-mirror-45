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


class ChatsSlice(Object):
    """Attributes:
        ID: ``0x9cd81144``

    Args:
        count: ``int`` ``32-bit``
        chats: List of either :obj:`ChatEmpty <DevLGram.api.types.ChatEmpty>`, :obj:`Chat <DevLGram.api.types.Chat>`, :obj:`ChatForbidden <DevLGram.api.types.ChatForbidden>`, :obj:`Channel <DevLGram.api.types.Channel>` or :obj:`ChannelForbidden <DevLGram.api.types.ChannelForbidden>`

    See Also:
        This object can be returned by :obj:`messages.GetChats <DevLGram.api.functions.messages.GetChats>`, :obj:`messages.GetCommonChats <DevLGram.api.functions.messages.GetCommonChats>`, :obj:`messages.GetAllChats <DevLGram.api.functions.messages.GetAllChats>`, :obj:`channels.GetChannels <DevLGram.api.functions.channels.GetChannels>`, :obj:`channels.GetAdminedPublicChannels <DevLGram.api.functions.channels.GetAdminedPublicChannels>` and :obj:`channels.GetLeftChannels <DevLGram.api.functions.channels.GetLeftChannels>`.
    """

    __slots__ = ["count", "chats"]

    ID = 0x9cd81144
    QUALNAME = "messages.ChatsSlice"

    def __init__(self, *, count: int, chats: list):
        self.count = count  # int
        self.chats = chats  # Vector<Chat>

    @staticmethod
    def read(b: BytesIO, *args) -> "ChatsSlice":
        # No flags
        
        count = Int.read(b)
        
        chats = Object.read(b)
        
        return ChatsSlice(count=count, chats=chats)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(Int(self.count))
        
        b.write(Vector(self.chats))
        
        return b.getvalue()
