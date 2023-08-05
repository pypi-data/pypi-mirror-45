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


class SetTyping(Object):
    """Attributes:
        ID: ``0xa3825e50``

    Args:
        peer: Either :obj:`InputPeerEmpty <DevLGram.api.types.InputPeerEmpty>`, :obj:`InputPeerSelf <DevLGram.api.types.InputPeerSelf>`, :obj:`InputPeerChat <DevLGram.api.types.InputPeerChat>`, :obj:`InputPeerUser <DevLGram.api.types.InputPeerUser>` or :obj:`InputPeerChannel <DevLGram.api.types.InputPeerChannel>`
        action: Either :obj:`SendMessageTypingAction <DevLGram.api.types.SendMessageTypingAction>`, :obj:`SendMessageCancelAction <DevLGram.api.types.SendMessageCancelAction>`, :obj:`SendMessageRecordVideoAction <DevLGram.api.types.SendMessageRecordVideoAction>`, :obj:`SendMessageUploadVideoAction <DevLGram.api.types.SendMessageUploadVideoAction>`, :obj:`SendMessageRecordAudioAction <DevLGram.api.types.SendMessageRecordAudioAction>`, :obj:`SendMessageUploadAudioAction <DevLGram.api.types.SendMessageUploadAudioAction>`, :obj:`SendMessageUploadPhotoAction <DevLGram.api.types.SendMessageUploadPhotoAction>`, :obj:`SendMessageUploadDocumentAction <DevLGram.api.types.SendMessageUploadDocumentAction>`, :obj:`SendMessageGeoLocationAction <DevLGram.api.types.SendMessageGeoLocationAction>`, :obj:`SendMessageChooseContactAction <DevLGram.api.types.SendMessageChooseContactAction>`, :obj:`SendMessageGamePlayAction <DevLGram.api.types.SendMessageGamePlayAction>`, :obj:`SendMessageRecordRoundAction <DevLGram.api.types.SendMessageRecordRoundAction>` or :obj:`SendMessageUploadRoundAction <DevLGram.api.types.SendMessageUploadRoundAction>`

    Raises:
        :obj:`RPCError <DevLGram.RPCError>`

    Returns:
        ``bool``
    """

    __slots__ = ["peer", "action"]

    ID = 0xa3825e50
    QUALNAME = "messages.SetTyping"

    def __init__(self, *, peer, action):
        self.peer = peer  # InputPeer
        self.action = action  # SendMessageAction

    @staticmethod
    def read(b: BytesIO, *args) -> "SetTyping":
        # No flags
        
        peer = Object.read(b)
        
        action = Object.read(b)
        
        return SetTyping(peer=peer, action=action)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(self.peer.write())
        
        b.write(self.action.write())
        
        return b.getvalue()
