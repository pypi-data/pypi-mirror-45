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


class AppUpdate(Object):
    """Attributes:
        ID: ``0x1da7158f``

    Args:
        id: ``int`` ``32-bit``
        version: ``str``
        text: ``str``
        entities: List of either :obj:`MessageEntityUnknown <DevLGram.api.types.MessageEntityUnknown>`, :obj:`MessageEntityMention <DevLGram.api.types.MessageEntityMention>`, :obj:`MessageEntityHashtag <DevLGram.api.types.MessageEntityHashtag>`, :obj:`MessageEntityBotCommand <DevLGram.api.types.MessageEntityBotCommand>`, :obj:`MessageEntityUrl <DevLGram.api.types.MessageEntityUrl>`, :obj:`MessageEntityEmail <DevLGram.api.types.MessageEntityEmail>`, :obj:`MessageEntityBold <DevLGram.api.types.MessageEntityBold>`, :obj:`MessageEntityItalic <DevLGram.api.types.MessageEntityItalic>`, :obj:`MessageEntityCode <DevLGram.api.types.MessageEntityCode>`, :obj:`MessageEntityPre <DevLGram.api.types.MessageEntityPre>`, :obj:`MessageEntityTextUrl <DevLGram.api.types.MessageEntityTextUrl>`, :obj:`MessageEntityMentionName <DevLGram.api.types.MessageEntityMentionName>`, :obj:`InputMessageEntityMentionName <DevLGram.api.types.InputMessageEntityMentionName>`, :obj:`MessageEntityPhone <DevLGram.api.types.MessageEntityPhone>` or :obj:`MessageEntityCashtag <DevLGram.api.types.MessageEntityCashtag>`
        popup (optional): ``bool``
        document (optional): Either :obj:`DocumentEmpty <DevLGram.api.types.DocumentEmpty>` or :obj:`Document <DevLGram.api.types.Document>`
        url (optional): ``str``

    See Also:
        This object can be returned by :obj:`help.GetAppUpdate <DevLGram.api.functions.help.GetAppUpdate>`.
    """

    __slots__ = ["id", "version", "text", "entities", "popup", "document", "url"]

    ID = 0x1da7158f
    QUALNAME = "help.AppUpdate"

    def __init__(self, *, id: int, version: str, text: str, entities: list, popup: bool = None, document=None, url: str = None):
        self.popup = popup  # flags.0?true
        self.id = id  # int
        self.version = version  # string
        self.text = text  # string
        self.entities = entities  # Vector<MessageEntity>
        self.document = document  # flags.1?Document
        self.url = url  # flags.2?string

    @staticmethod
    def read(b: BytesIO, *args) -> "AppUpdate":
        flags = Int.read(b)
        
        popup = True if flags & (1 << 0) else False
        id = Int.read(b)
        
        version = String.read(b)
        
        text = String.read(b)
        
        entities = Object.read(b)
        
        document = Object.read(b) if flags & (1 << 1) else None
        
        url = String.read(b) if flags & (1 << 2) else None
        return AppUpdate(id=id, version=version, text=text, entities=entities, popup=popup, document=document, url=url)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        flags = 0
        flags |= (1 << 0) if self.popup is not None else 0
        flags |= (1 << 1) if self.document is not None else 0
        flags |= (1 << 2) if self.url is not None else 0
        b.write(Int(flags))
        
        b.write(Int(self.id))
        
        b.write(String(self.version))
        
        b.write(String(self.text))
        
        b.write(Vector(self.entities))
        
        if self.document is not None:
            b.write(self.document.write())
        
        if self.url is not None:
            b.write(String(self.url))
        
        return b.getvalue()
