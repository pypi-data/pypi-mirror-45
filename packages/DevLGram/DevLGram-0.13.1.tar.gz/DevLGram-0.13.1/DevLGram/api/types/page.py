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


class Page(Object):
    """Attributes:
        ID: ``0xae891bec``

    Args:
        url: ``str``
        blocks: List of either :obj:`PageBlockUnsupported <DevLGram.api.types.PageBlockUnsupported>`, :obj:`PageBlockTitle <DevLGram.api.types.PageBlockTitle>`, :obj:`PageBlockSubtitle <DevLGram.api.types.PageBlockSubtitle>`, :obj:`PageBlockAuthorDate <DevLGram.api.types.PageBlockAuthorDate>`, :obj:`PageBlockHeader <DevLGram.api.types.PageBlockHeader>`, :obj:`PageBlockSubheader <DevLGram.api.types.PageBlockSubheader>`, :obj:`PageBlockParagraph <DevLGram.api.types.PageBlockParagraph>`, :obj:`PageBlockPreformatted <DevLGram.api.types.PageBlockPreformatted>`, :obj:`PageBlockFooter <DevLGram.api.types.PageBlockFooter>`, :obj:`PageBlockDivider <DevLGram.api.types.PageBlockDivider>`, :obj:`PageBlockAnchor <DevLGram.api.types.PageBlockAnchor>`, :obj:`PageBlockList <DevLGram.api.types.PageBlockList>`, :obj:`PageBlockBlockquote <DevLGram.api.types.PageBlockBlockquote>`, :obj:`PageBlockPullquote <DevLGram.api.types.PageBlockPullquote>`, :obj:`PageBlockPhoto <DevLGram.api.types.PageBlockPhoto>`, :obj:`PageBlockVideo <DevLGram.api.types.PageBlockVideo>`, :obj:`PageBlockCover <DevLGram.api.types.PageBlockCover>`, :obj:`PageBlockEmbed <DevLGram.api.types.PageBlockEmbed>`, :obj:`PageBlockEmbedPost <DevLGram.api.types.PageBlockEmbedPost>`, :obj:`PageBlockCollage <DevLGram.api.types.PageBlockCollage>`, :obj:`PageBlockSlideshow <DevLGram.api.types.PageBlockSlideshow>`, :obj:`PageBlockChannel <DevLGram.api.types.PageBlockChannel>`, :obj:`PageBlockAudio <DevLGram.api.types.PageBlockAudio>`, :obj:`PageBlockKicker <DevLGram.api.types.PageBlockKicker>`, :obj:`PageBlockTable <DevLGram.api.types.PageBlockTable>`, :obj:`PageBlockOrderedList <DevLGram.api.types.PageBlockOrderedList>`, :obj:`PageBlockDetails <DevLGram.api.types.PageBlockDetails>`, :obj:`PageBlockRelatedArticles <DevLGram.api.types.PageBlockRelatedArticles>` or :obj:`PageBlockMap <DevLGram.api.types.PageBlockMap>`
        photos: List of either :obj:`PhotoEmpty <DevLGram.api.types.PhotoEmpty>` or :obj:`Photo <DevLGram.api.types.Photo>`
        documents: List of either :obj:`DocumentEmpty <DevLGram.api.types.DocumentEmpty>` or :obj:`Document <DevLGram.api.types.Document>`
        part (optional): ``bool``
        rtl (optional): ``bool``
        v2 (optional): ``bool``
    """

    __slots__ = ["url", "blocks", "photos", "documents", "part", "rtl", "v2"]

    ID = 0xae891bec
    QUALNAME = "Page"

    def __init__(self, *, url: str, blocks: list, photos: list, documents: list, part: bool = None, rtl: bool = None, v2: bool = None):
        self.part = part  # flags.0?true
        self.rtl = rtl  # flags.1?true
        self.v2 = v2  # flags.2?true
        self.url = url  # string
        self.blocks = blocks  # Vector<PageBlock>
        self.photos = photos  # Vector<Photo>
        self.documents = documents  # Vector<Document>

    @staticmethod
    def read(b: BytesIO, *args) -> "Page":
        flags = Int.read(b)
        
        part = True if flags & (1 << 0) else False
        rtl = True if flags & (1 << 1) else False
        v2 = True if flags & (1 << 2) else False
        url = String.read(b)
        
        blocks = Object.read(b)
        
        photos = Object.read(b)
        
        documents = Object.read(b)
        
        return Page(url=url, blocks=blocks, photos=photos, documents=documents, part=part, rtl=rtl, v2=v2)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        flags = 0
        flags |= (1 << 0) if self.part is not None else 0
        flags |= (1 << 1) if self.rtl is not None else 0
        flags |= (1 << 2) if self.v2 is not None else 0
        b.write(Int(flags))
        
        b.write(String(self.url))
        
        b.write(Vector(self.blocks))
        
        b.write(Vector(self.photos))
        
        b.write(Vector(self.documents))
        
        return b.getvalue()
