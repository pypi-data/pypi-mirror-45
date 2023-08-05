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


class CreateChannel(Object):
    """Attributes:
        ID: ``0xf4893d7f``

    Args:
        title: ``str``
        about: ``str``
        broadcast (optional): ``bool``
        megagroup (optional): ``bool``

    Raises:
        :obj:`RPCError <DevLGram.RPCError>`

    Returns:
        Either :obj:`UpdatesTooLong <DevLGram.api.types.UpdatesTooLong>`, :obj:`UpdateShortMessage <DevLGram.api.types.UpdateShortMessage>`, :obj:`UpdateShortChatMessage <DevLGram.api.types.UpdateShortChatMessage>`, :obj:`UpdateShort <DevLGram.api.types.UpdateShort>`, :obj:`UpdatesCombined <DevLGram.api.types.UpdatesCombined>`, :obj:`Update <DevLGram.api.types.Update>` or :obj:`UpdateShortSentMessage <DevLGram.api.types.UpdateShortSentMessage>`
    """

    __slots__ = ["title", "about", "broadcast", "megagroup"]

    ID = 0xf4893d7f
    QUALNAME = "channels.CreateChannel"

    def __init__(self, *, title: str, about: str, broadcast: bool = None, megagroup: bool = None):
        self.broadcast = broadcast  # flags.0?true
        self.megagroup = megagroup  # flags.1?true
        self.title = title  # string
        self.about = about  # string

    @staticmethod
    def read(b: BytesIO, *args) -> "CreateChannel":
        flags = Int.read(b)
        
        broadcast = True if flags & (1 << 0) else False
        megagroup = True if flags & (1 << 1) else False
        title = String.read(b)
        
        about = String.read(b)
        
        return CreateChannel(title=title, about=about, broadcast=broadcast, megagroup=megagroup)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        flags = 0
        flags |= (1 << 0) if self.broadcast is not None else 0
        flags |= (1 << 1) if self.megagroup is not None else 0
        b.write(Int(flags))
        
        b.write(String(self.title))
        
        b.write(String(self.about))
        
        return b.getvalue()
