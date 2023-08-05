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


class ChannelMessages(Object):
    """Attributes:
        ID: ``0x99262e37``

    Args:
        pts: ``int`` ``32-bit``
        count: ``int`` ``32-bit``
        messages: List of either :obj:`MessageEmpty <DevLGram.api.types.MessageEmpty>`, :obj:`Message <DevLGram.api.types.Message>` or :obj:`MessageService <DevLGram.api.types.MessageService>`
        chats: List of either :obj:`ChatEmpty <DevLGram.api.types.ChatEmpty>`, :obj:`Chat <DevLGram.api.types.Chat>`, :obj:`ChatForbidden <DevLGram.api.types.ChatForbidden>`, :obj:`Channel <DevLGram.api.types.Channel>` or :obj:`ChannelForbidden <DevLGram.api.types.ChannelForbidden>`
        users: List of either :obj:`UserEmpty <DevLGram.api.types.UserEmpty>` or :obj:`User <DevLGram.api.types.User>`
        inexact (optional): ``bool``

    See Also:
        This object can be returned by :obj:`messages.GetMessages <DevLGram.api.functions.messages.GetMessages>`, :obj:`messages.GetHistory <DevLGram.api.functions.messages.GetHistory>`, :obj:`messages.Search <DevLGram.api.functions.messages.Search>`, :obj:`messages.SearchGlobal <DevLGram.api.functions.messages.SearchGlobal>`, :obj:`messages.GetUnreadMentions <DevLGram.api.functions.messages.GetUnreadMentions>`, :obj:`messages.GetRecentLocations <DevLGram.api.functions.messages.GetRecentLocations>` and :obj:`channels.GetMessages <DevLGram.api.functions.channels.GetMessages>`.
    """

    __slots__ = ["pts", "count", "messages", "chats", "users", "inexact"]

    ID = 0x99262e37
    QUALNAME = "messages.ChannelMessages"

    def __init__(self, *, pts: int, count: int, messages: list, chats: list, users: list, inexact: bool = None):
        self.inexact = inexact  # flags.1?true
        self.pts = pts  # int
        self.count = count  # int
        self.messages = messages  # Vector<Message>
        self.chats = chats  # Vector<Chat>
        self.users = users  # Vector<User>

    @staticmethod
    def read(b: BytesIO, *args) -> "ChannelMessages":
        flags = Int.read(b)
        
        inexact = True if flags & (1 << 1) else False
        pts = Int.read(b)
        
        count = Int.read(b)
        
        messages = Object.read(b)
        
        chats = Object.read(b)
        
        users = Object.read(b)
        
        return ChannelMessages(pts=pts, count=count, messages=messages, chats=chats, users=users, inexact=inexact)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        flags = 0
        flags |= (1 << 1) if self.inexact is not None else 0
        b.write(Int(flags))
        
        b.write(Int(self.pts))
        
        b.write(Int(self.count))
        
        b.write(Vector(self.messages))
        
        b.write(Vector(self.chats))
        
        b.write(Vector(self.users))
        
        return b.getvalue()
