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


class SendMultiMedia(Object):
    """Attributes:
        ID: ``0x2095512f``

    Args:
        peer: Either :obj:`InputPeerEmpty <DevLGram.api.types.InputPeerEmpty>`, :obj:`InputPeerSelf <DevLGram.api.types.InputPeerSelf>`, :obj:`InputPeerChat <DevLGram.api.types.InputPeerChat>`, :obj:`InputPeerUser <DevLGram.api.types.InputPeerUser>` or :obj:`InputPeerChannel <DevLGram.api.types.InputPeerChannel>`
        multi_media: List of :obj:`InputSingleMedia <DevLGram.api.types.InputSingleMedia>`
        silent (optional): ``bool``
        background (optional): ``bool``
        clear_draft (optional): ``bool``
        reply_to_msg_id (optional): ``int`` ``32-bit``

    Raises:
        :obj:`RPCError <DevLGram.RPCError>`

    Returns:
        Either :obj:`UpdatesTooLong <DevLGram.api.types.UpdatesTooLong>`, :obj:`UpdateShortMessage <DevLGram.api.types.UpdateShortMessage>`, :obj:`UpdateShortChatMessage <DevLGram.api.types.UpdateShortChatMessage>`, :obj:`UpdateShort <DevLGram.api.types.UpdateShort>`, :obj:`UpdatesCombined <DevLGram.api.types.UpdatesCombined>`, :obj:`Update <DevLGram.api.types.Update>` or :obj:`UpdateShortSentMessage <DevLGram.api.types.UpdateShortSentMessage>`
    """

    __slots__ = ["peer", "multi_media", "silent", "background", "clear_draft", "reply_to_msg_id"]

    ID = 0x2095512f
    QUALNAME = "messages.SendMultiMedia"

    def __init__(self, *, peer, multi_media: list, silent: bool = None, background: bool = None, clear_draft: bool = None, reply_to_msg_id: int = None):
        self.silent = silent  # flags.5?true
        self.background = background  # flags.6?true
        self.clear_draft = clear_draft  # flags.7?true
        self.peer = peer  # InputPeer
        self.reply_to_msg_id = reply_to_msg_id  # flags.0?int
        self.multi_media = multi_media  # Vector<InputSingleMedia>

    @staticmethod
    def read(b: BytesIO, *args) -> "SendMultiMedia":
        flags = Int.read(b)
        
        silent = True if flags & (1 << 5) else False
        background = True if flags & (1 << 6) else False
        clear_draft = True if flags & (1 << 7) else False
        peer = Object.read(b)
        
        reply_to_msg_id = Int.read(b) if flags & (1 << 0) else None
        multi_media = Object.read(b)
        
        return SendMultiMedia(peer=peer, multi_media=multi_media, silent=silent, background=background, clear_draft=clear_draft, reply_to_msg_id=reply_to_msg_id)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        flags = 0
        flags |= (1 << 5) if self.silent is not None else 0
        flags |= (1 << 6) if self.background is not None else 0
        flags |= (1 << 7) if self.clear_draft is not None else 0
        flags |= (1 << 0) if self.reply_to_msg_id is not None else 0
        b.write(Int(flags))
        
        b.write(self.peer.write())
        
        if self.reply_to_msg_id is not None:
            b.write(Int(self.reply_to_msg_id))
        
        b.write(Vector(self.multi_media))
        
        return b.getvalue()
