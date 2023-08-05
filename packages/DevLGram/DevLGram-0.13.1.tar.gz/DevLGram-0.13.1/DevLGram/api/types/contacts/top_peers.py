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


class TopPeers(Object):
    """Attributes:
        ID: ``0x70b772a8``

    Args:
        categories: List of :obj:`TopPeerCategoryPeers <DevLGram.api.types.TopPeerCategoryPeers>`
        chats: List of either :obj:`ChatEmpty <DevLGram.api.types.ChatEmpty>`, :obj:`Chat <DevLGram.api.types.Chat>`, :obj:`ChatForbidden <DevLGram.api.types.ChatForbidden>`, :obj:`Channel <DevLGram.api.types.Channel>` or :obj:`ChannelForbidden <DevLGram.api.types.ChannelForbidden>`
        users: List of either :obj:`UserEmpty <DevLGram.api.types.UserEmpty>` or :obj:`User <DevLGram.api.types.User>`

    See Also:
        This object can be returned by :obj:`contacts.GetTopPeers <DevLGram.api.functions.contacts.GetTopPeers>`.
    """

    __slots__ = ["categories", "chats", "users"]

    ID = 0x70b772a8
    QUALNAME = "contacts.TopPeers"

    def __init__(self, *, categories: list, chats: list, users: list):
        self.categories = categories  # Vector<TopPeerCategoryPeers>
        self.chats = chats  # Vector<Chat>
        self.users = users  # Vector<User>

    @staticmethod
    def read(b: BytesIO, *args) -> "TopPeers":
        # No flags
        
        categories = Object.read(b)
        
        chats = Object.read(b)
        
        users = Object.read(b)
        
        return TopPeers(categories=categories, chats=chats, users=users)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(Vector(self.categories))
        
        b.write(Vector(self.chats))
        
        b.write(Vector(self.users))
        
        return b.getvalue()
