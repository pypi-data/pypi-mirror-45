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


class UserInfo(Object):
    """Attributes:
        ID: ``0x01eb3758``

    Args:
        message: ``str``
        entities: List of either :obj:`MessageEntityUnknown <DevLGram.api.types.MessageEntityUnknown>`, :obj:`MessageEntityMention <DevLGram.api.types.MessageEntityMention>`, :obj:`MessageEntityHashtag <DevLGram.api.types.MessageEntityHashtag>`, :obj:`MessageEntityBotCommand <DevLGram.api.types.MessageEntityBotCommand>`, :obj:`MessageEntityUrl <DevLGram.api.types.MessageEntityUrl>`, :obj:`MessageEntityEmail <DevLGram.api.types.MessageEntityEmail>`, :obj:`MessageEntityBold <DevLGram.api.types.MessageEntityBold>`, :obj:`MessageEntityItalic <DevLGram.api.types.MessageEntityItalic>`, :obj:`MessageEntityCode <DevLGram.api.types.MessageEntityCode>`, :obj:`MessageEntityPre <DevLGram.api.types.MessageEntityPre>`, :obj:`MessageEntityTextUrl <DevLGram.api.types.MessageEntityTextUrl>`, :obj:`MessageEntityMentionName <DevLGram.api.types.MessageEntityMentionName>`, :obj:`InputMessageEntityMentionName <DevLGram.api.types.InputMessageEntityMentionName>`, :obj:`MessageEntityPhone <DevLGram.api.types.MessageEntityPhone>` or :obj:`MessageEntityCashtag <DevLGram.api.types.MessageEntityCashtag>`
        author: ``str``
        date: ``int`` ``32-bit``

    See Also:
        This object can be returned by :obj:`help.GetUserInfo <DevLGram.api.functions.help.GetUserInfo>` and :obj:`help.EditUserInfo <DevLGram.api.functions.help.EditUserInfo>`.
    """

    __slots__ = ["message", "entities", "author", "date"]

    ID = 0x01eb3758
    QUALNAME = "help.UserInfo"

    def __init__(self, *, message: str, entities: list, author: str, date: int):
        self.message = message  # string
        self.entities = entities  # Vector<MessageEntity>
        self.author = author  # string
        self.date = date  # int

    @staticmethod
    def read(b: BytesIO, *args) -> "UserInfo":
        # No flags
        
        message = String.read(b)
        
        entities = Object.read(b)
        
        author = String.read(b)
        
        date = Int.read(b)
        
        return UserInfo(message=message, entities=entities, author=author, date=date)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(String(self.message))
        
        b.write(Vector(self.entities))
        
        b.write(String(self.author))
        
        b.write(Int(self.date))
        
        return b.getvalue()
