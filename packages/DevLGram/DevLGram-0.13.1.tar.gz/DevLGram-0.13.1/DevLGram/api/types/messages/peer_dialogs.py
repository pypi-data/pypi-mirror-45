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


class PeerDialogs(Object):
    """Attributes:
        ID: ``0x3371c354``

    Args:
        dialogs: List of :obj:`Dialog <DevLGram.api.types.Dialog>`
        messages: List of either :obj:`MessageEmpty <DevLGram.api.types.MessageEmpty>`, :obj:`Message <DevLGram.api.types.Message>` or :obj:`MessageService <DevLGram.api.types.MessageService>`
        chats: List of either :obj:`ChatEmpty <DevLGram.api.types.ChatEmpty>`, :obj:`Chat <DevLGram.api.types.Chat>`, :obj:`ChatForbidden <DevLGram.api.types.ChatForbidden>`, :obj:`Channel <DevLGram.api.types.Channel>` or :obj:`ChannelForbidden <DevLGram.api.types.ChannelForbidden>`
        users: List of either :obj:`UserEmpty <DevLGram.api.types.UserEmpty>` or :obj:`User <DevLGram.api.types.User>`
        state: :obj:`updates.State <DevLGram.api.types.updates.State>`

    See Also:
        This object can be returned by :obj:`messages.GetPeerDialogs <DevLGram.api.functions.messages.GetPeerDialogs>` and :obj:`messages.GetPinnedDialogs <DevLGram.api.functions.messages.GetPinnedDialogs>`.
    """

    __slots__ = ["dialogs", "messages", "chats", "users", "state"]

    ID = 0x3371c354
    QUALNAME = "messages.PeerDialogs"

    def __init__(self, *, dialogs: list, messages: list, chats: list, users: list, state):
        self.dialogs = dialogs  # Vector<Dialog>
        self.messages = messages  # Vector<Message>
        self.chats = chats  # Vector<Chat>
        self.users = users  # Vector<User>
        self.state = state  # updates.State

    @staticmethod
    def read(b: BytesIO, *args) -> "PeerDialogs":
        # No flags
        
        dialogs = Object.read(b)
        
        messages = Object.read(b)
        
        chats = Object.read(b)
        
        users = Object.read(b)
        
        state = Object.read(b)
        
        return PeerDialogs(dialogs=dialogs, messages=messages, chats=chats, users=users, state=state)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(Vector(self.dialogs))
        
        b.write(Vector(self.messages))
        
        b.write(Vector(self.chats))
        
        b.write(Vector(self.users))
        
        b.write(self.state.write())
        
        return b.getvalue()
