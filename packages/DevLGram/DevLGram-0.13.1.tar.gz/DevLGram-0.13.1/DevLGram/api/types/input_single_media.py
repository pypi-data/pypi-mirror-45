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


class InputSingleMedia(Object):
    """Attributes:
        ID: ``0x1cc6e91f``

    Args:
        media: Either :obj:`InputMediaEmpty <DevLGram.api.types.InputMediaEmpty>`, :obj:`InputMediaUploadedPhoto <DevLGram.api.types.InputMediaUploadedPhoto>`, :obj:`InputMediaPhoto <DevLGram.api.types.InputMediaPhoto>`, :obj:`InputMediaGeoPoint <DevLGram.api.types.InputMediaGeoPoint>`, :obj:`InputMediaContact <DevLGram.api.types.InputMediaContact>`, :obj:`InputMediaUploadedDocument <DevLGram.api.types.InputMediaUploadedDocument>`, :obj:`InputMediaDocument <DevLGram.api.types.InputMediaDocument>`, :obj:`InputMediaVenue <DevLGram.api.types.InputMediaVenue>`, :obj:`InputMediaGifExternal <DevLGram.api.types.InputMediaGifExternal>`, :obj:`InputMediaPhotoExternal <DevLGram.api.types.InputMediaPhotoExternal>`, :obj:`InputMediaDocumentExternal <DevLGram.api.types.InputMediaDocumentExternal>`, :obj:`InputMediaGame <DevLGram.api.types.InputMediaGame>`, :obj:`InputMediaInvoice <DevLGram.api.types.InputMediaInvoice>`, :obj:`InputMediaGeoLive <DevLGram.api.types.InputMediaGeoLive>` or :obj:`InputMediaPoll <DevLGram.api.types.InputMediaPoll>`
        random_id: ``int`` ``64-bit``
        message: ``str``
        entities (optional): List of either :obj:`MessageEntityUnknown <DevLGram.api.types.MessageEntityUnknown>`, :obj:`MessageEntityMention <DevLGram.api.types.MessageEntityMention>`, :obj:`MessageEntityHashtag <DevLGram.api.types.MessageEntityHashtag>`, :obj:`MessageEntityBotCommand <DevLGram.api.types.MessageEntityBotCommand>`, :obj:`MessageEntityUrl <DevLGram.api.types.MessageEntityUrl>`, :obj:`MessageEntityEmail <DevLGram.api.types.MessageEntityEmail>`, :obj:`MessageEntityBold <DevLGram.api.types.MessageEntityBold>`, :obj:`MessageEntityItalic <DevLGram.api.types.MessageEntityItalic>`, :obj:`MessageEntityCode <DevLGram.api.types.MessageEntityCode>`, :obj:`MessageEntityPre <DevLGram.api.types.MessageEntityPre>`, :obj:`MessageEntityTextUrl <DevLGram.api.types.MessageEntityTextUrl>`, :obj:`MessageEntityMentionName <DevLGram.api.types.MessageEntityMentionName>`, :obj:`InputMessageEntityMentionName <DevLGram.api.types.InputMessageEntityMentionName>`, :obj:`MessageEntityPhone <DevLGram.api.types.MessageEntityPhone>` or :obj:`MessageEntityCashtag <DevLGram.api.types.MessageEntityCashtag>`
    """

    __slots__ = ["media", "random_id", "message", "entities"]

    ID = 0x1cc6e91f
    QUALNAME = "InputSingleMedia"

    def __init__(self, *, media, random_id: int, message: str, entities: list = None):
        self.media = media  # InputMedia
        self.random_id = random_id  # long
        self.message = message  # string
        self.entities = entities  # flags.0?Vector<MessageEntity>

    @staticmethod
    def read(b: BytesIO, *args) -> "InputSingleMedia":
        flags = Int.read(b)
        
        media = Object.read(b)
        
        random_id = Long.read(b)
        
        message = String.read(b)
        
        entities = Object.read(b) if flags & (1 << 0) else []
        
        return InputSingleMedia(media=media, random_id=random_id, message=message, entities=entities)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        flags = 0
        flags |= (1 << 0) if self.entities is not None else 0
        b.write(Int(flags))
        
        b.write(self.media.write())
        
        b.write(Long(self.random_id))
        
        b.write(String(self.message))
        
        if self.entities is not None:
            b.write(Vector(self.entities))
        
        return b.getvalue()
