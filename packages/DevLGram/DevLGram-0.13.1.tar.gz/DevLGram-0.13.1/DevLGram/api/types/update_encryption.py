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


class UpdateEncryption(Object):
    """Attributes:
        ID: ``0xb4a2e88d``

    Args:
        chat: Either :obj:`EncryptedChatEmpty <DevLGram.api.types.EncryptedChatEmpty>`, :obj:`EncryptedChatWaiting <DevLGram.api.types.EncryptedChatWaiting>`, :obj:`EncryptedChatRequested <DevLGram.api.types.EncryptedChatRequested>`, :obj:`EncryptedChat <DevLGram.api.types.EncryptedChat>` or :obj:`EncryptedChatDiscarded <DevLGram.api.types.EncryptedChatDiscarded>`
        date: ``int`` ``32-bit``
    """

    __slots__ = ["chat", "date"]

    ID = 0xb4a2e88d
    QUALNAME = "UpdateEncryption"

    def __init__(self, *, chat, date: int):
        self.chat = chat  # EncryptedChat
        self.date = date  # int

    @staticmethod
    def read(b: BytesIO, *args) -> "UpdateEncryption":
        # No flags
        
        chat = Object.read(b)
        
        date = Int.read(b)
        
        return UpdateEncryption(chat=chat, date=date)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(self.chat.write())
        
        b.write(Int(self.date))
        
        return b.getvalue()
