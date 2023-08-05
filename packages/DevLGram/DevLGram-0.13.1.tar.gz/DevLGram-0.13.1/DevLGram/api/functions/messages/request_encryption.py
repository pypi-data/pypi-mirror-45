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


class RequestEncryption(Object):
    """Attributes:
        ID: ``0xf64daf43``

    Args:
        user_id: Either :obj:`InputUserEmpty <DevLGram.api.types.InputUserEmpty>`, :obj:`InputUserSelf <DevLGram.api.types.InputUserSelf>` or :obj:`InputUser <DevLGram.api.types.InputUser>`
        random_id: ``int`` ``32-bit``
        g_a: ``bytes``

    Raises:
        :obj:`RPCError <DevLGram.RPCError>`

    Returns:
        Either :obj:`EncryptedChatEmpty <DevLGram.api.types.EncryptedChatEmpty>`, :obj:`EncryptedChatWaiting <DevLGram.api.types.EncryptedChatWaiting>`, :obj:`EncryptedChatRequested <DevLGram.api.types.EncryptedChatRequested>`, :obj:`EncryptedChat <DevLGram.api.types.EncryptedChat>` or :obj:`EncryptedChatDiscarded <DevLGram.api.types.EncryptedChatDiscarded>`
    """

    __slots__ = ["user_id", "random_id", "g_a"]

    ID = 0xf64daf43
    QUALNAME = "messages.RequestEncryption"

    def __init__(self, *, user_id, random_id: int, g_a: bytes):
        self.user_id = user_id  # InputUser
        self.random_id = random_id  # int
        self.g_a = g_a  # bytes

    @staticmethod
    def read(b: BytesIO, *args) -> "RequestEncryption":
        # No flags
        
        user_id = Object.read(b)
        
        random_id = Int.read(b)
        
        g_a = Bytes.read(b)
        
        return RequestEncryption(user_id=user_id, random_id=random_id, g_a=g_a)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(self.user_id.write())
        
        b.write(Int(self.random_id))
        
        b.write(Bytes(self.g_a))
        
        return b.getvalue()
