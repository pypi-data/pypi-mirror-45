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


class EditChatPhoto(Object):
    """Attributes:
        ID: ``0xca4c79d8``

    Args:
        chat_id: ``int`` ``32-bit``
        photo: Either :obj:`InputChatPhotoEmpty <DevLGram.api.types.InputChatPhotoEmpty>`, :obj:`InputChatUploadedPhoto <DevLGram.api.types.InputChatUploadedPhoto>` or :obj:`InputChatPhoto <DevLGram.api.types.InputChatPhoto>`

    Raises:
        :obj:`RPCError <DevLGram.RPCError>`

    Returns:
        Either :obj:`UpdatesTooLong <DevLGram.api.types.UpdatesTooLong>`, :obj:`UpdateShortMessage <DevLGram.api.types.UpdateShortMessage>`, :obj:`UpdateShortChatMessage <DevLGram.api.types.UpdateShortChatMessage>`, :obj:`UpdateShort <DevLGram.api.types.UpdateShort>`, :obj:`UpdatesCombined <DevLGram.api.types.UpdatesCombined>`, :obj:`Update <DevLGram.api.types.Update>` or :obj:`UpdateShortSentMessage <DevLGram.api.types.UpdateShortSentMessage>`
    """

    __slots__ = ["chat_id", "photo"]

    ID = 0xca4c79d8
    QUALNAME = "messages.EditChatPhoto"

    def __init__(self, *, chat_id: int, photo):
        self.chat_id = chat_id  # int
        self.photo = photo  # InputChatPhoto

    @staticmethod
    def read(b: BytesIO, *args) -> "EditChatPhoto":
        # No flags
        
        chat_id = Int.read(b)
        
        photo = Object.read(b)
        
        return EditChatPhoto(chat_id=chat_id, photo=photo)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(Int(self.chat_id))
        
        b.write(self.photo.write())
        
        return b.getvalue()
