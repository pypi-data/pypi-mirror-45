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


class GetWebPagePreview(Object):
    """Attributes:
        ID: ``0x8b68b0cc``

    Args:
        message: ``str``
        entities (optional): List of either :obj:`MessageEntityUnknown <DevLGram.api.types.MessageEntityUnknown>`, :obj:`MessageEntityMention <DevLGram.api.types.MessageEntityMention>`, :obj:`MessageEntityHashtag <DevLGram.api.types.MessageEntityHashtag>`, :obj:`MessageEntityBotCommand <DevLGram.api.types.MessageEntityBotCommand>`, :obj:`MessageEntityUrl <DevLGram.api.types.MessageEntityUrl>`, :obj:`MessageEntityEmail <DevLGram.api.types.MessageEntityEmail>`, :obj:`MessageEntityBold <DevLGram.api.types.MessageEntityBold>`, :obj:`MessageEntityItalic <DevLGram.api.types.MessageEntityItalic>`, :obj:`MessageEntityCode <DevLGram.api.types.MessageEntityCode>`, :obj:`MessageEntityPre <DevLGram.api.types.MessageEntityPre>`, :obj:`MessageEntityTextUrl <DevLGram.api.types.MessageEntityTextUrl>`, :obj:`MessageEntityMentionName <DevLGram.api.types.MessageEntityMentionName>`, :obj:`InputMessageEntityMentionName <DevLGram.api.types.InputMessageEntityMentionName>`, :obj:`MessageEntityPhone <DevLGram.api.types.MessageEntityPhone>` or :obj:`MessageEntityCashtag <DevLGram.api.types.MessageEntityCashtag>`

    Raises:
        :obj:`RPCError <DevLGram.RPCError>`

    Returns:
        Either :obj:`MessageMediaEmpty <DevLGram.api.types.MessageMediaEmpty>`, :obj:`MessageMediaPhoto <DevLGram.api.types.MessageMediaPhoto>`, :obj:`MessageMediaGeo <DevLGram.api.types.MessageMediaGeo>`, :obj:`MessageMediaContact <DevLGram.api.types.MessageMediaContact>`, :obj:`MessageMediaUnsupported <DevLGram.api.types.MessageMediaUnsupported>`, :obj:`MessageMediaDocument <DevLGram.api.types.MessageMediaDocument>`, :obj:`MessageMediaWebPage <DevLGram.api.types.MessageMediaWebPage>`, :obj:`MessageMediaVenue <DevLGram.api.types.MessageMediaVenue>`, :obj:`MessageMediaGame <DevLGram.api.types.MessageMediaGame>`, :obj:`MessageMediaInvoice <DevLGram.api.types.MessageMediaInvoice>`, :obj:`MessageMediaGeoLive <DevLGram.api.types.MessageMediaGeoLive>` or :obj:`MessageMediaPoll <DevLGram.api.types.MessageMediaPoll>`
    """

    __slots__ = ["message", "entities"]

    ID = 0x8b68b0cc
    QUALNAME = "messages.GetWebPagePreview"

    def __init__(self, *, message: str, entities: list = None):
        self.message = message  # string
        self.entities = entities  # flags.3?Vector<MessageEntity>

    @staticmethod
    def read(b: BytesIO, *args) -> "GetWebPagePreview":
        flags = Int.read(b)
        
        message = String.read(b)
        
        entities = Object.read(b) if flags & (1 << 3) else []
        
        return GetWebPagePreview(message=message, entities=entities)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        flags = 0
        flags |= (1 << 3) if self.entities is not None else 0
        b.write(Int(flags))
        
        b.write(String(self.message))
        
        if self.entities is not None:
            b.write(Vector(self.entities))
        
        return b.getvalue()
