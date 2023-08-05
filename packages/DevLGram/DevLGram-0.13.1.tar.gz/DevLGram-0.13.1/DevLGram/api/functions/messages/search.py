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


class Search(Object):
    """Attributes:
        ID: ``0x8614ef68``

    Args:
        peer: Either :obj:`InputPeerEmpty <DevLGram.api.types.InputPeerEmpty>`, :obj:`InputPeerSelf <DevLGram.api.types.InputPeerSelf>`, :obj:`InputPeerChat <DevLGram.api.types.InputPeerChat>`, :obj:`InputPeerUser <DevLGram.api.types.InputPeerUser>` or :obj:`InputPeerChannel <DevLGram.api.types.InputPeerChannel>`
        q: ``str``
        filter: Either :obj:`InputMessagesFilterEmpty <DevLGram.api.types.InputMessagesFilterEmpty>`, :obj:`InputMessagesFilterPhotos <DevLGram.api.types.InputMessagesFilterPhotos>`, :obj:`InputMessagesFilterVideo <DevLGram.api.types.InputMessagesFilterVideo>`, :obj:`InputMessagesFilterPhotoVideo <DevLGram.api.types.InputMessagesFilterPhotoVideo>`, :obj:`InputMessagesFilterDocument <DevLGram.api.types.InputMessagesFilterDocument>`, :obj:`InputMessagesFilterUrl <DevLGram.api.types.InputMessagesFilterUrl>`, :obj:`InputMessagesFilterGif <DevLGram.api.types.InputMessagesFilterGif>`, :obj:`InputMessagesFilterVoice <DevLGram.api.types.InputMessagesFilterVoice>`, :obj:`InputMessagesFilterMusic <DevLGram.api.types.InputMessagesFilterMusic>`, :obj:`InputMessagesFilterChatPhotos <DevLGram.api.types.InputMessagesFilterChatPhotos>`, :obj:`InputMessagesFilterPhoneCalls <DevLGram.api.types.InputMessagesFilterPhoneCalls>`, :obj:`InputMessagesFilterRoundVoice <DevLGram.api.types.InputMessagesFilterRoundVoice>`, :obj:`InputMessagesFilterRoundVideo <DevLGram.api.types.InputMessagesFilterRoundVideo>`, :obj:`InputMessagesFilterMyMentions <DevLGram.api.types.InputMessagesFilterMyMentions>`, :obj:`InputMessagesFilterGeo <DevLGram.api.types.InputMessagesFilterGeo>` or :obj:`InputMessagesFilterContacts <DevLGram.api.types.InputMessagesFilterContacts>`
        min_date: ``int`` ``32-bit``
        max_date: ``int`` ``32-bit``
        offset_id: ``int`` ``32-bit``
        add_offset: ``int`` ``32-bit``
        limit: ``int`` ``32-bit``
        max_id: ``int`` ``32-bit``
        min_id: ``int`` ``32-bit``
        hash: ``int`` ``32-bit``
        from_id (optional): Either :obj:`InputUserEmpty <DevLGram.api.types.InputUserEmpty>`, :obj:`InputUserSelf <DevLGram.api.types.InputUserSelf>` or :obj:`InputUser <DevLGram.api.types.InputUser>`

    Raises:
        :obj:`RPCError <DevLGram.RPCError>`

    Returns:
        Either :obj:`messages.Messages <DevLGram.api.types.messages.Messages>`, :obj:`messages.MessagesSlice <DevLGram.api.types.messages.MessagesSlice>`, :obj:`messages.ChannelMessages <DevLGram.api.types.messages.ChannelMessages>` or :obj:`messages.MessagesNotModified <DevLGram.api.types.messages.MessagesNotModified>`
    """

    __slots__ = ["peer", "q", "filter", "min_date", "max_date", "offset_id", "add_offset", "limit", "max_id", "min_id", "hash", "from_id"]

    ID = 0x8614ef68
    QUALNAME = "messages.Search"

    def __init__(self, *, peer, q: str, filter, min_date: int, max_date: int, offset_id: int, add_offset: int, limit: int, max_id: int, min_id: int, hash: int, from_id=None):
        self.peer = peer  # InputPeer
        self.q = q  # string
        self.from_id = from_id  # flags.0?InputUser
        self.filter = filter  # MessagesFilter
        self.min_date = min_date  # int
        self.max_date = max_date  # int
        self.offset_id = offset_id  # int
        self.add_offset = add_offset  # int
        self.limit = limit  # int
        self.max_id = max_id  # int
        self.min_id = min_id  # int
        self.hash = hash  # int

    @staticmethod
    def read(b: BytesIO, *args) -> "Search":
        flags = Int.read(b)
        
        peer = Object.read(b)
        
        q = String.read(b)
        
        from_id = Object.read(b) if flags & (1 << 0) else None
        
        filter = Object.read(b)
        
        min_date = Int.read(b)
        
        max_date = Int.read(b)
        
        offset_id = Int.read(b)
        
        add_offset = Int.read(b)
        
        limit = Int.read(b)
        
        max_id = Int.read(b)
        
        min_id = Int.read(b)
        
        hash = Int.read(b)
        
        return Search(peer=peer, q=q, filter=filter, min_date=min_date, max_date=max_date, offset_id=offset_id, add_offset=add_offset, limit=limit, max_id=max_id, min_id=min_id, hash=hash, from_id=from_id)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        flags = 0
        flags |= (1 << 0) if self.from_id is not None else 0
        b.write(Int(flags))
        
        b.write(self.peer.write())
        
        b.write(String(self.q))
        
        if self.from_id is not None:
            b.write(self.from_id.write())
        
        b.write(self.filter.write())
        
        b.write(Int(self.min_date))
        
        b.write(Int(self.max_date))
        
        b.write(Int(self.offset_id))
        
        b.write(Int(self.add_offset))
        
        b.write(Int(self.limit))
        
        b.write(Int(self.max_id))
        
        b.write(Int(self.min_id))
        
        b.write(Int(self.hash))
        
        return b.getvalue()
