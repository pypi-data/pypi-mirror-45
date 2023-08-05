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


class UpdateChatUserTyping(Object):
    """Attributes:
        ID: ``0x9a65ea1f``

    Args:
        chat_id: ``int`` ``32-bit``
        user_id: ``int`` ``32-bit``
        action: Either :obj:`SendMessageTypingAction <DevLGram.api.types.SendMessageTypingAction>`, :obj:`SendMessageCancelAction <DevLGram.api.types.SendMessageCancelAction>`, :obj:`SendMessageRecordVideoAction <DevLGram.api.types.SendMessageRecordVideoAction>`, :obj:`SendMessageUploadVideoAction <DevLGram.api.types.SendMessageUploadVideoAction>`, :obj:`SendMessageRecordAudioAction <DevLGram.api.types.SendMessageRecordAudioAction>`, :obj:`SendMessageUploadAudioAction <DevLGram.api.types.SendMessageUploadAudioAction>`, :obj:`SendMessageUploadPhotoAction <DevLGram.api.types.SendMessageUploadPhotoAction>`, :obj:`SendMessageUploadDocumentAction <DevLGram.api.types.SendMessageUploadDocumentAction>`, :obj:`SendMessageGeoLocationAction <DevLGram.api.types.SendMessageGeoLocationAction>`, :obj:`SendMessageChooseContactAction <DevLGram.api.types.SendMessageChooseContactAction>`, :obj:`SendMessageGamePlayAction <DevLGram.api.types.SendMessageGamePlayAction>`, :obj:`SendMessageRecordRoundAction <DevLGram.api.types.SendMessageRecordRoundAction>` or :obj:`SendMessageUploadRoundAction <DevLGram.api.types.SendMessageUploadRoundAction>`
    """

    __slots__ = ["chat_id", "user_id", "action"]

    ID = 0x9a65ea1f
    QUALNAME = "UpdateChatUserTyping"

    def __init__(self, *, chat_id: int, user_id: int, action):
        self.chat_id = chat_id  # int
        self.user_id = user_id  # int
        self.action = action  # SendMessageAction

    @staticmethod
    def read(b: BytesIO, *args) -> "UpdateChatUserTyping":
        # No flags
        
        chat_id = Int.read(b)
        
        user_id = Int.read(b)
        
        action = Object.read(b)
        
        return UpdateChatUserTyping(chat_id=chat_id, user_id=user_id, action=action)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(Int(self.chat_id))
        
        b.write(Int(self.user_id))
        
        b.write(self.action.write())
        
        return b.getvalue()
