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


class ChatInviteAlready(Object):
    """Attributes:
        ID: ``0x5a686d7c``

    Args:
        chat: Either :obj:`ChatEmpty <DevLGram.api.types.ChatEmpty>`, :obj:`Chat <DevLGram.api.types.Chat>`, :obj:`ChatForbidden <DevLGram.api.types.ChatForbidden>`, :obj:`Channel <DevLGram.api.types.Channel>` or :obj:`ChannelForbidden <DevLGram.api.types.ChannelForbidden>`

    See Also:
        This object can be returned by :obj:`messages.CheckChatInvite <DevLGram.api.functions.messages.CheckChatInvite>`.
    """

    __slots__ = ["chat"]

    ID = 0x5a686d7c
    QUALNAME = "ChatInviteAlready"

    def __init__(self, *, chat):
        self.chat = chat  # Chat

    @staticmethod
    def read(b: BytesIO, *args) -> "ChatInviteAlready":
        # No flags
        
        chat = Object.read(b)
        
        return ChatInviteAlready(chat=chat)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(self.chat.write())
        
        return b.getvalue()
