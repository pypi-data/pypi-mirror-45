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


class InputBotInlineMessageText(Object):
    """Attributes:
        ID: ``0x3dcd7a87``

    Args:
        message: ``str``
        no_webpage (optional): ``bool``
        entities (optional): List of either :obj:`MessageEntityUnknown <DevLGram.api.types.MessageEntityUnknown>`, :obj:`MessageEntityMention <DevLGram.api.types.MessageEntityMention>`, :obj:`MessageEntityHashtag <DevLGram.api.types.MessageEntityHashtag>`, :obj:`MessageEntityBotCommand <DevLGram.api.types.MessageEntityBotCommand>`, :obj:`MessageEntityUrl <DevLGram.api.types.MessageEntityUrl>`, :obj:`MessageEntityEmail <DevLGram.api.types.MessageEntityEmail>`, :obj:`MessageEntityBold <DevLGram.api.types.MessageEntityBold>`, :obj:`MessageEntityItalic <DevLGram.api.types.MessageEntityItalic>`, :obj:`MessageEntityCode <DevLGram.api.types.MessageEntityCode>`, :obj:`MessageEntityPre <DevLGram.api.types.MessageEntityPre>`, :obj:`MessageEntityTextUrl <DevLGram.api.types.MessageEntityTextUrl>`, :obj:`MessageEntityMentionName <DevLGram.api.types.MessageEntityMentionName>`, :obj:`InputMessageEntityMentionName <DevLGram.api.types.InputMessageEntityMentionName>`, :obj:`MessageEntityPhone <DevLGram.api.types.MessageEntityPhone>` or :obj:`MessageEntityCashtag <DevLGram.api.types.MessageEntityCashtag>`
        reply_markup (optional): Either :obj:`ReplyKeyboardHide <DevLGram.api.types.ReplyKeyboardHide>`, :obj:`ReplyKeyboardForceReply <DevLGram.api.types.ReplyKeyboardForceReply>`, :obj:`ReplyKeyboardMarkup <DevLGram.api.types.ReplyKeyboardMarkup>` or :obj:`ReplyInlineMarkup <DevLGram.api.types.ReplyInlineMarkup>`
    """

    __slots__ = ["message", "no_webpage", "entities", "reply_markup"]

    ID = 0x3dcd7a87
    QUALNAME = "InputBotInlineMessageText"

    def __init__(self, *, message: str, no_webpage: bool = None, entities: list = None, reply_markup=None):
        self.no_webpage = no_webpage  # flags.0?true
        self.message = message  # string
        self.entities = entities  # flags.1?Vector<MessageEntity>
        self.reply_markup = reply_markup  # flags.2?ReplyMarkup

    @staticmethod
    def read(b: BytesIO, *args) -> "InputBotInlineMessageText":
        flags = Int.read(b)
        
        no_webpage = True if flags & (1 << 0) else False
        message = String.read(b)
        
        entities = Object.read(b) if flags & (1 << 1) else []
        
        reply_markup = Object.read(b) if flags & (1 << 2) else None
        
        return InputBotInlineMessageText(message=message, no_webpage=no_webpage, entities=entities, reply_markup=reply_markup)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        flags = 0
        flags |= (1 << 0) if self.no_webpage is not None else 0
        flags |= (1 << 1) if self.entities is not None else 0
        flags |= (1 << 2) if self.reply_markup is not None else 0
        b.write(Int(flags))
        
        b.write(String(self.message))
        
        if self.entities is not None:
            b.write(Vector(self.entities))
        
        if self.reply_markup is not None:
            b.write(self.reply_markup.write())
        
        return b.getvalue()
