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


class UploadMedia(Object):
    """Attributes:
        ID: ``0x519bc2b1``

    Args:
        peer: Either :obj:`InputPeerEmpty <DevLGram.api.types.InputPeerEmpty>`, :obj:`InputPeerSelf <DevLGram.api.types.InputPeerSelf>`, :obj:`InputPeerChat <DevLGram.api.types.InputPeerChat>`, :obj:`InputPeerUser <DevLGram.api.types.InputPeerUser>` or :obj:`InputPeerChannel <DevLGram.api.types.InputPeerChannel>`
        media: Either :obj:`InputMediaEmpty <DevLGram.api.types.InputMediaEmpty>`, :obj:`InputMediaUploadedPhoto <DevLGram.api.types.InputMediaUploadedPhoto>`, :obj:`InputMediaPhoto <DevLGram.api.types.InputMediaPhoto>`, :obj:`InputMediaGeoPoint <DevLGram.api.types.InputMediaGeoPoint>`, :obj:`InputMediaContact <DevLGram.api.types.InputMediaContact>`, :obj:`InputMediaUploadedDocument <DevLGram.api.types.InputMediaUploadedDocument>`, :obj:`InputMediaDocument <DevLGram.api.types.InputMediaDocument>`, :obj:`InputMediaVenue <DevLGram.api.types.InputMediaVenue>`, :obj:`InputMediaGifExternal <DevLGram.api.types.InputMediaGifExternal>`, :obj:`InputMediaPhotoExternal <DevLGram.api.types.InputMediaPhotoExternal>`, :obj:`InputMediaDocumentExternal <DevLGram.api.types.InputMediaDocumentExternal>`, :obj:`InputMediaGame <DevLGram.api.types.InputMediaGame>`, :obj:`InputMediaInvoice <DevLGram.api.types.InputMediaInvoice>`, :obj:`InputMediaGeoLive <DevLGram.api.types.InputMediaGeoLive>` or :obj:`InputMediaPoll <DevLGram.api.types.InputMediaPoll>`

    Raises:
        :obj:`RPCError <DevLGram.RPCError>`

    Returns:
        Either :obj:`MessageMediaEmpty <DevLGram.api.types.MessageMediaEmpty>`, :obj:`MessageMediaPhoto <DevLGram.api.types.MessageMediaPhoto>`, :obj:`MessageMediaGeo <DevLGram.api.types.MessageMediaGeo>`, :obj:`MessageMediaContact <DevLGram.api.types.MessageMediaContact>`, :obj:`MessageMediaUnsupported <DevLGram.api.types.MessageMediaUnsupported>`, :obj:`MessageMediaDocument <DevLGram.api.types.MessageMediaDocument>`, :obj:`MessageMediaWebPage <DevLGram.api.types.MessageMediaWebPage>`, :obj:`MessageMediaVenue <DevLGram.api.types.MessageMediaVenue>`, :obj:`MessageMediaGame <DevLGram.api.types.MessageMediaGame>`, :obj:`MessageMediaInvoice <DevLGram.api.types.MessageMediaInvoice>`, :obj:`MessageMediaGeoLive <DevLGram.api.types.MessageMediaGeoLive>` or :obj:`MessageMediaPoll <DevLGram.api.types.MessageMediaPoll>`
    """

    __slots__ = ["peer", "media"]

    ID = 0x519bc2b1
    QUALNAME = "messages.UploadMedia"

    def __init__(self, *, peer, media):
        self.peer = peer  # InputPeer
        self.media = media  # InputMedia

    @staticmethod
    def read(b: BytesIO, *args) -> "UploadMedia":
        # No flags
        
        peer = Object.read(b)
        
        media = Object.read(b)
        
        return UploadMedia(peer=peer, media=media)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(self.peer.write())
        
        b.write(self.media.write())
        
        return b.getvalue()
