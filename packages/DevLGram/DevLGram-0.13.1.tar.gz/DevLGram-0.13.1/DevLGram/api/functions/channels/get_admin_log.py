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


class GetAdminLog(Object):
    """Attributes:
        ID: ``0x33ddf480``

    Args:
        channel: Either :obj:`InputChannelEmpty <DevLGram.api.types.InputChannelEmpty>` or :obj:`InputChannel <DevLGram.api.types.InputChannel>`
        q: ``str``
        max_id: ``int`` ``64-bit``
        min_id: ``int`` ``64-bit``
        limit: ``int`` ``32-bit``
        events_filter (optional): :obj:`ChannelAdminLogEventsFilter <DevLGram.api.types.ChannelAdminLogEventsFilter>`
        admins (optional): List of either :obj:`InputUserEmpty <DevLGram.api.types.InputUserEmpty>`, :obj:`InputUserSelf <DevLGram.api.types.InputUserSelf>` or :obj:`InputUser <DevLGram.api.types.InputUser>`

    Raises:
        :obj:`RPCError <DevLGram.RPCError>`

    Returns:
        :obj:`channels.AdminLogResults <DevLGram.api.types.channels.AdminLogResults>`
    """

    __slots__ = ["channel", "q", "max_id", "min_id", "limit", "events_filter", "admins"]

    ID = 0x33ddf480
    QUALNAME = "channels.GetAdminLog"

    def __init__(self, *, channel, q: str, max_id: int, min_id: int, limit: int, events_filter=None, admins: list = None):
        self.channel = channel  # InputChannel
        self.q = q  # string
        self.events_filter = events_filter  # flags.0?ChannelAdminLogEventsFilter
        self.admins = admins  # flags.1?Vector<InputUser>
        self.max_id = max_id  # long
        self.min_id = min_id  # long
        self.limit = limit  # int

    @staticmethod
    def read(b: BytesIO, *args) -> "GetAdminLog":
        flags = Int.read(b)
        
        channel = Object.read(b)
        
        q = String.read(b)
        
        events_filter = Object.read(b) if flags & (1 << 0) else None
        
        admins = Object.read(b) if flags & (1 << 1) else []
        
        max_id = Long.read(b)
        
        min_id = Long.read(b)
        
        limit = Int.read(b)
        
        return GetAdminLog(channel=channel, q=q, max_id=max_id, min_id=min_id, limit=limit, events_filter=events_filter, admins=admins)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        flags = 0
        flags |= (1 << 0) if self.events_filter is not None else 0
        flags |= (1 << 1) if self.admins is not None else 0
        b.write(Int(flags))
        
        b.write(self.channel.write())
        
        b.write(String(self.q))
        
        if self.events_filter is not None:
            b.write(self.events_filter.write())
        
        if self.admins is not None:
            b.write(Vector(self.admins))
        
        b.write(Long(self.max_id))
        
        b.write(Long(self.min_id))
        
        b.write(Int(self.limit))
        
        return b.getvalue()
