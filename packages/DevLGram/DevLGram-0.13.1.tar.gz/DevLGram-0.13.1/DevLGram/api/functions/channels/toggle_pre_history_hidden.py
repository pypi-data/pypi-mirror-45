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


class TogglePreHistoryHidden(Object):
    """Attributes:
        ID: ``0xeabbb94c``

    Args:
        channel: Either :obj:`InputChannelEmpty <DevLGram.api.types.InputChannelEmpty>` or :obj:`InputChannel <DevLGram.api.types.InputChannel>`
        enabled: ``bool``

    Raises:
        :obj:`RPCError <DevLGram.RPCError>`

    Returns:
        Either :obj:`UpdatesTooLong <DevLGram.api.types.UpdatesTooLong>`, :obj:`UpdateShortMessage <DevLGram.api.types.UpdateShortMessage>`, :obj:`UpdateShortChatMessage <DevLGram.api.types.UpdateShortChatMessage>`, :obj:`UpdateShort <DevLGram.api.types.UpdateShort>`, :obj:`UpdatesCombined <DevLGram.api.types.UpdatesCombined>`, :obj:`Update <DevLGram.api.types.Update>` or :obj:`UpdateShortSentMessage <DevLGram.api.types.UpdateShortSentMessage>`
    """

    __slots__ = ["channel", "enabled"]

    ID = 0xeabbb94c
    QUALNAME = "channels.TogglePreHistoryHidden"

    def __init__(self, *, channel, enabled: bool):
        self.channel = channel  # InputChannel
        self.enabled = enabled  # Bool

    @staticmethod
    def read(b: BytesIO, *args) -> "TogglePreHistoryHidden":
        # No flags
        
        channel = Object.read(b)
        
        enabled = Bool.read(b)
        
        return TogglePreHistoryHidden(channel=channel, enabled=enabled)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(self.channel.write())
        
        b.write(Bool(self.enabled))
        
        return b.getvalue()
