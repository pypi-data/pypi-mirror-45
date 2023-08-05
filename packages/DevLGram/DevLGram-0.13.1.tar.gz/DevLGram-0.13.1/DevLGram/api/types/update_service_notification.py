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


class UpdateServiceNotification(Object):
    """Attributes:
        ID: ``0xebe46819``

    Args:
        type: ``str``
        message: ``str``
        media: Either :obj:`MessageMediaEmpty <DevLGram.api.types.MessageMediaEmpty>`, :obj:`MessageMediaPhoto <DevLGram.api.types.MessageMediaPhoto>`, :obj:`MessageMediaGeo <DevLGram.api.types.MessageMediaGeo>`, :obj:`MessageMediaContact <DevLGram.api.types.MessageMediaContact>`, :obj:`MessageMediaUnsupported <DevLGram.api.types.MessageMediaUnsupported>`, :obj:`MessageMediaDocument <DevLGram.api.types.MessageMediaDocument>`, :obj:`MessageMediaWebPage <DevLGram.api.types.MessageMediaWebPage>`, :obj:`MessageMediaVenue <DevLGram.api.types.MessageMediaVenue>`, :obj:`MessageMediaGame <DevLGram.api.types.MessageMediaGame>`, :obj:`MessageMediaInvoice <DevLGram.api.types.MessageMediaInvoice>`, :obj:`MessageMediaGeoLive <DevLGram.api.types.MessageMediaGeoLive>` or :obj:`MessageMediaPoll <DevLGram.api.types.MessageMediaPoll>`
        entities: List of either :obj:`MessageEntityUnknown <DevLGram.api.types.MessageEntityUnknown>`, :obj:`MessageEntityMention <DevLGram.api.types.MessageEntityMention>`, :obj:`MessageEntityHashtag <DevLGram.api.types.MessageEntityHashtag>`, :obj:`MessageEntityBotCommand <DevLGram.api.types.MessageEntityBotCommand>`, :obj:`MessageEntityUrl <DevLGram.api.types.MessageEntityUrl>`, :obj:`MessageEntityEmail <DevLGram.api.types.MessageEntityEmail>`, :obj:`MessageEntityBold <DevLGram.api.types.MessageEntityBold>`, :obj:`MessageEntityItalic <DevLGram.api.types.MessageEntityItalic>`, :obj:`MessageEntityCode <DevLGram.api.types.MessageEntityCode>`, :obj:`MessageEntityPre <DevLGram.api.types.MessageEntityPre>`, :obj:`MessageEntityTextUrl <DevLGram.api.types.MessageEntityTextUrl>`, :obj:`MessageEntityMentionName <DevLGram.api.types.MessageEntityMentionName>`, :obj:`InputMessageEntityMentionName <DevLGram.api.types.InputMessageEntityMentionName>`, :obj:`MessageEntityPhone <DevLGram.api.types.MessageEntityPhone>` or :obj:`MessageEntityCashtag <DevLGram.api.types.MessageEntityCashtag>`
        popup (optional): ``bool``
        inbox_date (optional): ``int`` ``32-bit``
    """

    __slots__ = ["type", "message", "media", "entities", "popup", "inbox_date"]

    ID = 0xebe46819
    QUALNAME = "UpdateServiceNotification"

    def __init__(self, *, type: str, message: str, media, entities: list, popup: bool = None, inbox_date: int = None):
        self.popup = popup  # flags.0?true
        self.inbox_date = inbox_date  # flags.1?int
        self.type = type  # string
        self.message = message  # string
        self.media = media  # MessageMedia
        self.entities = entities  # Vector<MessageEntity>

    @staticmethod
    def read(b: BytesIO, *args) -> "UpdateServiceNotification":
        flags = Int.read(b)
        
        popup = True if flags & (1 << 0) else False
        inbox_date = Int.read(b) if flags & (1 << 1) else None
        type = String.read(b)
        
        message = String.read(b)
        
        media = Object.read(b)
        
        entities = Object.read(b)
        
        return UpdateServiceNotification(type=type, message=message, media=media, entities=entities, popup=popup, inbox_date=inbox_date)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        flags = 0
        flags |= (1 << 0) if self.popup is not None else 0
        flags |= (1 << 1) if self.inbox_date is not None else 0
        b.write(Int(flags))
        
        if self.inbox_date is not None:
            b.write(Int(self.inbox_date))
        
        b.write(String(self.type))
        
        b.write(String(self.message))
        
        b.write(self.media.write())
        
        b.write(Vector(self.entities))
        
        return b.getvalue()
