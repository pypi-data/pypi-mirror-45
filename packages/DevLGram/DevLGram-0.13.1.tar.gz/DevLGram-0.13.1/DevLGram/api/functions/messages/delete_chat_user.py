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


class DeleteChatUser(Object):
    """Attributes:
        ID: ``0xe0611f16``

    Args:
        chat_id: ``int`` ``32-bit``
        user_id: Either :obj:`InputUserEmpty <DevLGram.api.types.InputUserEmpty>`, :obj:`InputUserSelf <DevLGram.api.types.InputUserSelf>` or :obj:`InputUser <DevLGram.api.types.InputUser>`

    Raises:
        :obj:`RPCError <DevLGram.RPCError>`

    Returns:
        Either :obj:`UpdatesTooLong <DevLGram.api.types.UpdatesTooLong>`, :obj:`UpdateShortMessage <DevLGram.api.types.UpdateShortMessage>`, :obj:`UpdateShortChatMessage <DevLGram.api.types.UpdateShortChatMessage>`, :obj:`UpdateShort <DevLGram.api.types.UpdateShort>`, :obj:`UpdatesCombined <DevLGram.api.types.UpdatesCombined>`, :obj:`Update <DevLGram.api.types.Update>` or :obj:`UpdateShortSentMessage <DevLGram.api.types.UpdateShortSentMessage>`
    """

    __slots__ = ["chat_id", "user_id"]

    ID = 0xe0611f16
    QUALNAME = "messages.DeleteChatUser"

    def __init__(self, *, chat_id: int, user_id):
        self.chat_id = chat_id  # int
        self.user_id = user_id  # InputUser

    @staticmethod
    def read(b: BytesIO, *args) -> "DeleteChatUser":
        # No flags
        
        chat_id = Int.read(b)
        
        user_id = Object.read(b)
        
        return DeleteChatUser(chat_id=chat_id, user_id=user_id)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(Int(self.chat_id))
        
        b.write(self.user_id.write())
        
        return b.getvalue()
