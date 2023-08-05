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


class SetStickers(Object):
    """Attributes:
        ID: ``0xea8ca4f9``

    Args:
        channel: Either :obj:`InputChannelEmpty <DevLGram.api.types.InputChannelEmpty>` or :obj:`InputChannel <DevLGram.api.types.InputChannel>`
        stickerset: Either :obj:`InputStickerSetEmpty <DevLGram.api.types.InputStickerSetEmpty>`, :obj:`InputStickerSetID <DevLGram.api.types.InputStickerSetID>` or :obj:`InputStickerSetShortName <DevLGram.api.types.InputStickerSetShortName>`

    Raises:
        :obj:`RPCError <DevLGram.RPCError>`

    Returns:
        ``bool``
    """

    __slots__ = ["channel", "stickerset"]

    ID = 0xea8ca4f9
    QUALNAME = "channels.SetStickers"

    def __init__(self, *, channel, stickerset):
        self.channel = channel  # InputChannel
        self.stickerset = stickerset  # InputStickerSet

    @staticmethod
    def read(b: BytesIO, *args) -> "SetStickers":
        # No flags
        
        channel = Object.read(b)
        
        stickerset = Object.read(b)
        
        return SetStickers(channel=channel, stickerset=stickerset)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(self.channel.write())
        
        b.write(self.stickerset.write())
        
        return b.getvalue()
