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


class ChatFull(Object):
    """Attributes:
        ID: ``0xe5d7d19c``

    Args:
        full_chat: Either :obj:`ChatFull <DevLGram.api.types.ChatFull>` or :obj:`ChannelFull <DevLGram.api.types.ChannelFull>`
        chats: List of either :obj:`ChatEmpty <DevLGram.api.types.ChatEmpty>`, :obj:`Chat <DevLGram.api.types.Chat>`, :obj:`ChatForbidden <DevLGram.api.types.ChatForbidden>`, :obj:`Channel <DevLGram.api.types.Channel>` or :obj:`ChannelForbidden <DevLGram.api.types.ChannelForbidden>`
        users: List of either :obj:`UserEmpty <DevLGram.api.types.UserEmpty>` or :obj:`User <DevLGram.api.types.User>`

    See Also:
        This object can be returned by :obj:`messages.GetFullChat <DevLGram.api.functions.messages.GetFullChat>` and :obj:`channels.GetFullChannel <DevLGram.api.functions.channels.GetFullChannel>`.
    """

    __slots__ = ["full_chat", "chats", "users"]

    ID = 0xe5d7d19c
    QUALNAME = "messages.ChatFull"

    def __init__(self, *, full_chat, chats: list, users: list):
        self.full_chat = full_chat  # ChatFull
        self.chats = chats  # Vector<Chat>
        self.users = users  # Vector<User>

    @staticmethod
    def read(b: BytesIO, *args) -> "ChatFull":
        # No flags
        
        full_chat = Object.read(b)
        
        chats = Object.read(b)
        
        users = Object.read(b)
        
        return ChatFull(full_chat=full_chat, chats=chats, users=users)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(self.full_chat.write())
        
        b.write(Vector(self.chats))
        
        b.write(Vector(self.users))
        
        return b.getvalue()
