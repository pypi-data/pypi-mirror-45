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


class Messages(Object):
    """Attributes:
        ID: ``0x8c718e87``

    Args:
        messages: List of either :obj:`MessageEmpty <DevLGram.api.types.MessageEmpty>`, :obj:`Message <DevLGram.api.types.Message>` or :obj:`MessageService <DevLGram.api.types.MessageService>`
        chats: List of either :obj:`ChatEmpty <DevLGram.api.types.ChatEmpty>`, :obj:`Chat <DevLGram.api.types.Chat>`, :obj:`ChatForbidden <DevLGram.api.types.ChatForbidden>`, :obj:`Channel <DevLGram.api.types.Channel>` or :obj:`ChannelForbidden <DevLGram.api.types.ChannelForbidden>`
        users: List of either :obj:`UserEmpty <DevLGram.api.types.UserEmpty>` or :obj:`User <DevLGram.api.types.User>`

    See Also:
        This object can be returned by :obj:`messages.GetMessages <DevLGram.api.functions.messages.GetMessages>`, :obj:`messages.GetHistory <DevLGram.api.functions.messages.GetHistory>`, :obj:`messages.Search <DevLGram.api.functions.messages.Search>`, :obj:`messages.SearchGlobal <DevLGram.api.functions.messages.SearchGlobal>`, :obj:`messages.GetUnreadMentions <DevLGram.api.functions.messages.GetUnreadMentions>`, :obj:`messages.GetRecentLocations <DevLGram.api.functions.messages.GetRecentLocations>` and :obj:`channels.GetMessages <DevLGram.api.functions.channels.GetMessages>`.
    """

    __slots__ = ["messages", "chats", "users"]

    ID = 0x8c718e87
    QUALNAME = "messages.Messages"

    def __init__(self, *, messages: list, chats: list, users: list):
        self.messages = messages  # Vector<Message>
        self.chats = chats  # Vector<Chat>
        self.users = users  # Vector<User>

    @staticmethod
    def read(b: BytesIO, *args) -> "Messages":
        # No flags
        
        messages = Object.read(b)
        
        chats = Object.read(b)
        
        users = Object.read(b)
        
        return Messages(messages=messages, chats=chats, users=users)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(Vector(self.messages))
        
        b.write(Vector(self.chats))
        
        b.write(Vector(self.users))
        
        return b.getvalue()
