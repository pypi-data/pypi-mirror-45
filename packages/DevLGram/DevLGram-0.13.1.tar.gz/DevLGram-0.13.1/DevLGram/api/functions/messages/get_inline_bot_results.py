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


class GetInlineBotResults(Object):
    """Attributes:
        ID: ``0x514e999d``

    Args:
        bot: Either :obj:`InputUserEmpty <DevLGram.api.types.InputUserEmpty>`, :obj:`InputUserSelf <DevLGram.api.types.InputUserSelf>` or :obj:`InputUser <DevLGram.api.types.InputUser>`
        peer: Either :obj:`InputPeerEmpty <DevLGram.api.types.InputPeerEmpty>`, :obj:`InputPeerSelf <DevLGram.api.types.InputPeerSelf>`, :obj:`InputPeerChat <DevLGram.api.types.InputPeerChat>`, :obj:`InputPeerUser <DevLGram.api.types.InputPeerUser>` or :obj:`InputPeerChannel <DevLGram.api.types.InputPeerChannel>`
        query: ``str``
        offset: ``str``
        geo_point (optional): Either :obj:`InputGeoPointEmpty <DevLGram.api.types.InputGeoPointEmpty>` or :obj:`InputGeoPoint <DevLGram.api.types.InputGeoPoint>`

    Raises:
        :obj:`RPCError <DevLGram.RPCError>`

    Returns:
        :obj:`messages.BotResults <DevLGram.api.types.messages.BotResults>`
    """

    __slots__ = ["bot", "peer", "query", "offset", "geo_point"]

    ID = 0x514e999d
    QUALNAME = "messages.GetInlineBotResults"

    def __init__(self, *, bot, peer, query: str, offset: str, geo_point=None):
        self.bot = bot  # InputUser
        self.peer = peer  # InputPeer
        self.geo_point = geo_point  # flags.0?InputGeoPoint
        self.query = query  # string
        self.offset = offset  # string

    @staticmethod
    def read(b: BytesIO, *args) -> "GetInlineBotResults":
        flags = Int.read(b)
        
        bot = Object.read(b)
        
        peer = Object.read(b)
        
        geo_point = Object.read(b) if flags & (1 << 0) else None
        
        query = String.read(b)
        
        offset = String.read(b)
        
        return GetInlineBotResults(bot=bot, peer=peer, query=query, offset=offset, geo_point=geo_point)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        flags = 0
        flags |= (1 << 0) if self.geo_point is not None else 0
        b.write(Int(flags))
        
        b.write(self.bot.write())
        
        b.write(self.peer.write())
        
        if self.geo_point is not None:
            b.write(self.geo_point.write())
        
        b.write(String(self.query))
        
        b.write(String(self.offset))
        
        return b.getvalue()
