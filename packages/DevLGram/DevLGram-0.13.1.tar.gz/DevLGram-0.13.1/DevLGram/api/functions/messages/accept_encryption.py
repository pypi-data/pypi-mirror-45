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


class AcceptEncryption(Object):
    """Attributes:
        ID: ``0x3dbc0415``

    Args:
        peer: :obj:`InputEncryptedChat <DevLGram.api.types.InputEncryptedChat>`
        g_b: ``bytes``
        key_fingerprint: ``int`` ``64-bit``

    Raises:
        :obj:`RPCError <DevLGram.RPCError>`

    Returns:
        Either :obj:`EncryptedChatEmpty <DevLGram.api.types.EncryptedChatEmpty>`, :obj:`EncryptedChatWaiting <DevLGram.api.types.EncryptedChatWaiting>`, :obj:`EncryptedChatRequested <DevLGram.api.types.EncryptedChatRequested>`, :obj:`EncryptedChat <DevLGram.api.types.EncryptedChat>` or :obj:`EncryptedChatDiscarded <DevLGram.api.types.EncryptedChatDiscarded>`
    """

    __slots__ = ["peer", "g_b", "key_fingerprint"]

    ID = 0x3dbc0415
    QUALNAME = "messages.AcceptEncryption"

    def __init__(self, *, peer, g_b: bytes, key_fingerprint: int):
        self.peer = peer  # InputEncryptedChat
        self.g_b = g_b  # bytes
        self.key_fingerprint = key_fingerprint  # long

    @staticmethod
    def read(b: BytesIO, *args) -> "AcceptEncryption":
        # No flags
        
        peer = Object.read(b)
        
        g_b = Bytes.read(b)
        
        key_fingerprint = Long.read(b)
        
        return AcceptEncryption(peer=peer, g_b=g_b, key_fingerprint=key_fingerprint)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(self.peer.write())
        
        b.write(Bytes(self.g_b))
        
        b.write(Long(self.key_fingerprint))
        
        return b.getvalue()
