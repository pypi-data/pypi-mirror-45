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


class MessageService(Object):
    """Attributes:
        ID: ``0x9e19a1f6``

    Args:
        id: ``int`` ``32-bit``
        to_id: Either :obj:`PeerUser <DevLGram.api.types.PeerUser>`, :obj:`PeerChat <DevLGram.api.types.PeerChat>` or :obj:`PeerChannel <DevLGram.api.types.PeerChannel>`
        date: ``int`` ``32-bit``
        action: Either :obj:`MessageActionEmpty <DevLGram.api.types.MessageActionEmpty>`, :obj:`MessageActionChatCreate <DevLGram.api.types.MessageActionChatCreate>`, :obj:`MessageActionChatEditTitle <DevLGram.api.types.MessageActionChatEditTitle>`, :obj:`MessageActionChatEditPhoto <DevLGram.api.types.MessageActionChatEditPhoto>`, :obj:`MessageActionChatDeletePhoto <DevLGram.api.types.MessageActionChatDeletePhoto>`, :obj:`MessageActionChatAddUser <DevLGram.api.types.MessageActionChatAddUser>`, :obj:`MessageActionChatDeleteUser <DevLGram.api.types.MessageActionChatDeleteUser>`, :obj:`MessageActionChatJoinedByLink <DevLGram.api.types.MessageActionChatJoinedByLink>`, :obj:`MessageActionChannelCreate <DevLGram.api.types.MessageActionChannelCreate>`, :obj:`MessageActionChatMigrateTo <DevLGram.api.types.MessageActionChatMigrateTo>`, :obj:`MessageActionChannelMigrateFrom <DevLGram.api.types.MessageActionChannelMigrateFrom>`, :obj:`MessageActionPinMessage <DevLGram.api.types.MessageActionPinMessage>`, :obj:`MessageActionHistoryClear <DevLGram.api.types.MessageActionHistoryClear>`, :obj:`MessageActionGameScore <DevLGram.api.types.MessageActionGameScore>`, :obj:`MessageActionPaymentSentMe <DevLGram.api.types.MessageActionPaymentSentMe>`, :obj:`MessageActionPaymentSent <DevLGram.api.types.MessageActionPaymentSent>`, :obj:`MessageActionPhoneCall <DevLGram.api.types.MessageActionPhoneCall>`, :obj:`MessageActionScreenshotTaken <DevLGram.api.types.MessageActionScreenshotTaken>`, :obj:`MessageActionCustomAction <DevLGram.api.types.MessageActionCustomAction>`, :obj:`MessageActionBotAllowed <DevLGram.api.types.MessageActionBotAllowed>`, :obj:`MessageActionSecureValuesSentMe <DevLGram.api.types.MessageActionSecureValuesSentMe>`, :obj:`MessageActionSecureValuesSent <DevLGram.api.types.MessageActionSecureValuesSent>` or :obj:`MessageActionContactSignUp <DevLGram.api.types.MessageActionContactSignUp>`
        out (optional): ``bool``
        mentioned (optional): ``bool``
        media_unread (optional): ``bool``
        silent (optional): ``bool``
        post (optional): ``bool``
        from_id (optional): ``int`` ``32-bit``
        reply_to_msg_id (optional): ``int`` ``32-bit``
    """

    __slots__ = ["id", "to_id", "date", "action", "out", "mentioned", "media_unread", "silent", "post", "from_id", "reply_to_msg_id"]

    ID = 0x9e19a1f6
    QUALNAME = "MessageService"

    def __init__(self, *, id: int, to_id, date: int, action, out: bool = None, mentioned: bool = None, media_unread: bool = None, silent: bool = None, post: bool = None, from_id: int = None, reply_to_msg_id: int = None):
        self.out = out  # flags.1?true
        self.mentioned = mentioned  # flags.4?true
        self.media_unread = media_unread  # flags.5?true
        self.silent = silent  # flags.13?true
        self.post = post  # flags.14?true
        self.id = id  # int
        self.from_id = from_id  # flags.8?int
        self.to_id = to_id  # Peer
        self.reply_to_msg_id = reply_to_msg_id  # flags.3?int
        self.date = date  # int
        self.action = action  # MessageAction

    @staticmethod
    def read(b: BytesIO, *args) -> "MessageService":
        flags = Int.read(b)
        
        out = True if flags & (1 << 1) else False
        mentioned = True if flags & (1 << 4) else False
        media_unread = True if flags & (1 << 5) else False
        silent = True if flags & (1 << 13) else False
        post = True if flags & (1 << 14) else False
        id = Int.read(b)
        
        from_id = Int.read(b) if flags & (1 << 8) else None
        to_id = Object.read(b)
        
        reply_to_msg_id = Int.read(b) if flags & (1 << 3) else None
        date = Int.read(b)
        
        action = Object.read(b)
        
        return MessageService(id=id, to_id=to_id, date=date, action=action, out=out, mentioned=mentioned, media_unread=media_unread, silent=silent, post=post, from_id=from_id, reply_to_msg_id=reply_to_msg_id)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        flags = 0
        flags |= (1 << 1) if self.out is not None else 0
        flags |= (1 << 4) if self.mentioned is not None else 0
        flags |= (1 << 5) if self.media_unread is not None else 0
        flags |= (1 << 13) if self.silent is not None else 0
        flags |= (1 << 14) if self.post is not None else 0
        flags |= (1 << 8) if self.from_id is not None else 0
        flags |= (1 << 3) if self.reply_to_msg_id is not None else 0
        b.write(Int(flags))
        
        b.write(Int(self.id))
        
        if self.from_id is not None:
            b.write(Int(self.from_id))
        
        b.write(self.to_id.write())
        
        if self.reply_to_msg_id is not None:
            b.write(Int(self.reply_to_msg_id))
        
        b.write(Int(self.date))
        
        b.write(self.action.write())
        
        return b.getvalue()
