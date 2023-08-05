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


class SaveDraft(Object):
    """Attributes:
        ID: ``0xbc39e14b``

    Args:
        peer: Either :obj:`InputPeerEmpty <DevLGram.api.types.InputPeerEmpty>`, :obj:`InputPeerSelf <DevLGram.api.types.InputPeerSelf>`, :obj:`InputPeerChat <DevLGram.api.types.InputPeerChat>`, :obj:`InputPeerUser <DevLGram.api.types.InputPeerUser>` or :obj:`InputPeerChannel <DevLGram.api.types.InputPeerChannel>`
        message: ``str``
        no_webpage (optional): ``bool``
        reply_to_msg_id (optional): ``int`` ``32-bit``
        entities (optional): List of either :obj:`MessageEntityUnknown <DevLGram.api.types.MessageEntityUnknown>`, :obj:`MessageEntityMention <DevLGram.api.types.MessageEntityMention>`, :obj:`MessageEntityHashtag <DevLGram.api.types.MessageEntityHashtag>`, :obj:`MessageEntityBotCommand <DevLGram.api.types.MessageEntityBotCommand>`, :obj:`MessageEntityUrl <DevLGram.api.types.MessageEntityUrl>`, :obj:`MessageEntityEmail <DevLGram.api.types.MessageEntityEmail>`, :obj:`MessageEntityBold <DevLGram.api.types.MessageEntityBold>`, :obj:`MessageEntityItalic <DevLGram.api.types.MessageEntityItalic>`, :obj:`MessageEntityCode <DevLGram.api.types.MessageEntityCode>`, :obj:`MessageEntityPre <DevLGram.api.types.MessageEntityPre>`, :obj:`MessageEntityTextUrl <DevLGram.api.types.MessageEntityTextUrl>`, :obj:`MessageEntityMentionName <DevLGram.api.types.MessageEntityMentionName>`, :obj:`InputMessageEntityMentionName <DevLGram.api.types.InputMessageEntityMentionName>`, :obj:`MessageEntityPhone <DevLGram.api.types.MessageEntityPhone>` or :obj:`MessageEntityCashtag <DevLGram.api.types.MessageEntityCashtag>`

    Raises:
        :obj:`RPCError <DevLGram.RPCError>`

    Returns:
        ``bool``
    """

    __slots__ = ["peer", "message", "no_webpage", "reply_to_msg_id", "entities"]

    ID = 0xbc39e14b
    QUALNAME = "messages.SaveDraft"

    def __init__(self, *, peer, message: str, no_webpage: bool = None, reply_to_msg_id: int = None, entities: list = None):
        self.no_webpage = no_webpage  # flags.1?true
        self.reply_to_msg_id = reply_to_msg_id  # flags.0?int
        self.peer = peer  # InputPeer
        self.message = message  # string
        self.entities = entities  # flags.3?Vector<MessageEntity>

    @staticmethod
    def read(b: BytesIO, *args) -> "SaveDraft":
        flags = Int.read(b)
        
        no_webpage = True if flags & (1 << 1) else False
        reply_to_msg_id = Int.read(b) if flags & (1 << 0) else None
        peer = Object.read(b)
        
        message = String.read(b)
        
        entities = Object.read(b) if flags & (1 << 3) else []
        
        return SaveDraft(peer=peer, message=message, no_webpage=no_webpage, reply_to_msg_id=reply_to_msg_id, entities=entities)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        flags = 0
        flags |= (1 << 1) if self.no_webpage is not None else 0
        flags |= (1 << 0) if self.reply_to_msg_id is not None else 0
        flags |= (1 << 3) if self.entities is not None else 0
        b.write(Int(flags))
        
        if self.reply_to_msg_id is not None:
            b.write(Int(self.reply_to_msg_id))
        
        b.write(self.peer.write())
        
        b.write(String(self.message))
        
        if self.entities is not None:
            b.write(Vector(self.entities))
        
        return b.getvalue()
