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


class EditBanned(Object):
    """Attributes:
        ID: ``0x72796912``

    Args:
        channel: Either :obj:`InputChannelEmpty <DevLGram.api.types.InputChannelEmpty>` or :obj:`InputChannel <DevLGram.api.types.InputChannel>`
        user_id: Either :obj:`InputUserEmpty <DevLGram.api.types.InputUserEmpty>`, :obj:`InputUserSelf <DevLGram.api.types.InputUserSelf>` or :obj:`InputUser <DevLGram.api.types.InputUser>`
        banned_rights: :obj:`ChatBannedRights <DevLGram.api.types.ChatBannedRights>`

    Raises:
        :obj:`RPCError <DevLGram.RPCError>`

    Returns:
        Either :obj:`UpdatesTooLong <DevLGram.api.types.UpdatesTooLong>`, :obj:`UpdateShortMessage <DevLGram.api.types.UpdateShortMessage>`, :obj:`UpdateShortChatMessage <DevLGram.api.types.UpdateShortChatMessage>`, :obj:`UpdateShort <DevLGram.api.types.UpdateShort>`, :obj:`UpdatesCombined <DevLGram.api.types.UpdatesCombined>`, :obj:`Update <DevLGram.api.types.Update>` or :obj:`UpdateShortSentMessage <DevLGram.api.types.UpdateShortSentMessage>`
    """

    __slots__ = ["channel", "user_id", "banned_rights"]

    ID = 0x72796912
    QUALNAME = "channels.EditBanned"

    def __init__(self, *, channel, user_id, banned_rights):
        self.channel = channel  # InputChannel
        self.user_id = user_id  # InputUser
        self.banned_rights = banned_rights  # ChatBannedRights

    @staticmethod
    def read(b: BytesIO, *args) -> "EditBanned":
        # No flags
        
        channel = Object.read(b)
        
        user_id = Object.read(b)
        
        banned_rights = Object.read(b)
        
        return EditBanned(channel=channel, user_id=user_id, banned_rights=banned_rights)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(self.channel.write())
        
        b.write(self.user_id.write())
        
        b.write(self.banned_rights.write())
        
        return b.getvalue()
