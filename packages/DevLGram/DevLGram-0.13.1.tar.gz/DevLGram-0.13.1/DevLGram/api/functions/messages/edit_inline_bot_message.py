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


class EditInlineBotMessage(Object):
    """Attributes:
        ID: ``0x83557dba``

    Args:
        id: :obj:`InputBotInlineMessageID <DevLGram.api.types.InputBotInlineMessageID>`
        no_webpage (optional): ``bool``
        message (optional): ``str``
        media (optional): Either :obj:`InputMediaEmpty <DevLGram.api.types.InputMediaEmpty>`, :obj:`InputMediaUploadedPhoto <DevLGram.api.types.InputMediaUploadedPhoto>`, :obj:`InputMediaPhoto <DevLGram.api.types.InputMediaPhoto>`, :obj:`InputMediaGeoPoint <DevLGram.api.types.InputMediaGeoPoint>`, :obj:`InputMediaContact <DevLGram.api.types.InputMediaContact>`, :obj:`InputMediaUploadedDocument <DevLGram.api.types.InputMediaUploadedDocument>`, :obj:`InputMediaDocument <DevLGram.api.types.InputMediaDocument>`, :obj:`InputMediaVenue <DevLGram.api.types.InputMediaVenue>`, :obj:`InputMediaGifExternal <DevLGram.api.types.InputMediaGifExternal>`, :obj:`InputMediaPhotoExternal <DevLGram.api.types.InputMediaPhotoExternal>`, :obj:`InputMediaDocumentExternal <DevLGram.api.types.InputMediaDocumentExternal>`, :obj:`InputMediaGame <DevLGram.api.types.InputMediaGame>`, :obj:`InputMediaInvoice <DevLGram.api.types.InputMediaInvoice>`, :obj:`InputMediaGeoLive <DevLGram.api.types.InputMediaGeoLive>` or :obj:`InputMediaPoll <DevLGram.api.types.InputMediaPoll>`
        reply_markup (optional): Either :obj:`ReplyKeyboardHide <DevLGram.api.types.ReplyKeyboardHide>`, :obj:`ReplyKeyboardForceReply <DevLGram.api.types.ReplyKeyboardForceReply>`, :obj:`ReplyKeyboardMarkup <DevLGram.api.types.ReplyKeyboardMarkup>` or :obj:`ReplyInlineMarkup <DevLGram.api.types.ReplyInlineMarkup>`
        entities (optional): List of either :obj:`MessageEntityUnknown <DevLGram.api.types.MessageEntityUnknown>`, :obj:`MessageEntityMention <DevLGram.api.types.MessageEntityMention>`, :obj:`MessageEntityHashtag <DevLGram.api.types.MessageEntityHashtag>`, :obj:`MessageEntityBotCommand <DevLGram.api.types.MessageEntityBotCommand>`, :obj:`MessageEntityUrl <DevLGram.api.types.MessageEntityUrl>`, :obj:`MessageEntityEmail <DevLGram.api.types.MessageEntityEmail>`, :obj:`MessageEntityBold <DevLGram.api.types.MessageEntityBold>`, :obj:`MessageEntityItalic <DevLGram.api.types.MessageEntityItalic>`, :obj:`MessageEntityCode <DevLGram.api.types.MessageEntityCode>`, :obj:`MessageEntityPre <DevLGram.api.types.MessageEntityPre>`, :obj:`MessageEntityTextUrl <DevLGram.api.types.MessageEntityTextUrl>`, :obj:`MessageEntityMentionName <DevLGram.api.types.MessageEntityMentionName>`, :obj:`InputMessageEntityMentionName <DevLGram.api.types.InputMessageEntityMentionName>`, :obj:`MessageEntityPhone <DevLGram.api.types.MessageEntityPhone>` or :obj:`MessageEntityCashtag <DevLGram.api.types.MessageEntityCashtag>`

    Raises:
        :obj:`RPCError <DevLGram.RPCError>`

    Returns:
        ``bool``
    """

    __slots__ = ["id", "no_webpage", "message", "media", "reply_markup", "entities"]

    ID = 0x83557dba
    QUALNAME = "messages.EditInlineBotMessage"

    def __init__(self, *, id, no_webpage: bool = None, message: str = None, media=None, reply_markup=None, entities: list = None):
        self.no_webpage = no_webpage  # flags.1?true
        self.id = id  # InputBotInlineMessageID
        self.message = message  # flags.11?string
        self.media = media  # flags.14?InputMedia
        self.reply_markup = reply_markup  # flags.2?ReplyMarkup
        self.entities = entities  # flags.3?Vector<MessageEntity>

    @staticmethod
    def read(b: BytesIO, *args) -> "EditInlineBotMessage":
        flags = Int.read(b)
        
        no_webpage = True if flags & (1 << 1) else False
        id = Object.read(b)
        
        message = String.read(b) if flags & (1 << 11) else None
        media = Object.read(b) if flags & (1 << 14) else None
        
        reply_markup = Object.read(b) if flags & (1 << 2) else None
        
        entities = Object.read(b) if flags & (1 << 3) else []
        
        return EditInlineBotMessage(id=id, no_webpage=no_webpage, message=message, media=media, reply_markup=reply_markup, entities=entities)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        flags = 0
        flags |= (1 << 1) if self.no_webpage is not None else 0
        flags |= (1 << 11) if self.message is not None else 0
        flags |= (1 << 14) if self.media is not None else 0
        flags |= (1 << 2) if self.reply_markup is not None else 0
        flags |= (1 << 3) if self.entities is not None else 0
        b.write(Int(flags))
        
        b.write(self.id.write())
        
        if self.message is not None:
            b.write(String(self.message))
        
        if self.media is not None:
            b.write(self.media.write())
        
        if self.reply_markup is not None:
            b.write(self.reply_markup.write())
        
        if self.entities is not None:
            b.write(Vector(self.entities))
        
        return b.getvalue()
