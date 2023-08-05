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


class PageBlockEmbedPost(Object):
    """Attributes:
        ID: ``0xf259a80b``

    Args:
        url: ``str``
        webpage_id: ``int`` ``64-bit``
        author_photo_id: ``int`` ``64-bit``
        author: ``str``
        date: ``int`` ``32-bit``
        blocks: List of either :obj:`PageBlockUnsupported <DevLGram.api.types.PageBlockUnsupported>`, :obj:`PageBlockTitle <DevLGram.api.types.PageBlockTitle>`, :obj:`PageBlockSubtitle <DevLGram.api.types.PageBlockSubtitle>`, :obj:`PageBlockAuthorDate <DevLGram.api.types.PageBlockAuthorDate>`, :obj:`PageBlockHeader <DevLGram.api.types.PageBlockHeader>`, :obj:`PageBlockSubheader <DevLGram.api.types.PageBlockSubheader>`, :obj:`PageBlockParagraph <DevLGram.api.types.PageBlockParagraph>`, :obj:`PageBlockPreformatted <DevLGram.api.types.PageBlockPreformatted>`, :obj:`PageBlockFooter <DevLGram.api.types.PageBlockFooter>`, :obj:`PageBlockDivider <DevLGram.api.types.PageBlockDivider>`, :obj:`PageBlockAnchor <DevLGram.api.types.PageBlockAnchor>`, :obj:`PageBlockList <DevLGram.api.types.PageBlockList>`, :obj:`PageBlockBlockquote <DevLGram.api.types.PageBlockBlockquote>`, :obj:`PageBlockPullquote <DevLGram.api.types.PageBlockPullquote>`, :obj:`PageBlockPhoto <DevLGram.api.types.PageBlockPhoto>`, :obj:`PageBlockVideo <DevLGram.api.types.PageBlockVideo>`, :obj:`PageBlockCover <DevLGram.api.types.PageBlockCover>`, :obj:`PageBlockEmbed <DevLGram.api.types.PageBlockEmbed>`, :obj:`PageBlockEmbedPost <DevLGram.api.types.PageBlockEmbedPost>`, :obj:`PageBlockCollage <DevLGram.api.types.PageBlockCollage>`, :obj:`PageBlockSlideshow <DevLGram.api.types.PageBlockSlideshow>`, :obj:`PageBlockChannel <DevLGram.api.types.PageBlockChannel>`, :obj:`PageBlockAudio <DevLGram.api.types.PageBlockAudio>`, :obj:`PageBlockKicker <DevLGram.api.types.PageBlockKicker>`, :obj:`PageBlockTable <DevLGram.api.types.PageBlockTable>`, :obj:`PageBlockOrderedList <DevLGram.api.types.PageBlockOrderedList>`, :obj:`PageBlockDetails <DevLGram.api.types.PageBlockDetails>`, :obj:`PageBlockRelatedArticles <DevLGram.api.types.PageBlockRelatedArticles>` or :obj:`PageBlockMap <DevLGram.api.types.PageBlockMap>`
        caption: :obj:`PageCaption <DevLGram.api.types.PageCaption>`
    """

    __slots__ = ["url", "webpage_id", "author_photo_id", "author", "date", "blocks", "caption"]

    ID = 0xf259a80b
    QUALNAME = "PageBlockEmbedPost"

    def __init__(self, *, url: str, webpage_id: int, author_photo_id: int, author: str, date: int, blocks: list, caption):
        self.url = url  # string
        self.webpage_id = webpage_id  # long
        self.author_photo_id = author_photo_id  # long
        self.author = author  # string
        self.date = date  # int
        self.blocks = blocks  # Vector<PageBlock>
        self.caption = caption  # PageCaption

    @staticmethod
    def read(b: BytesIO, *args) -> "PageBlockEmbedPost":
        # No flags
        
        url = String.read(b)
        
        webpage_id = Long.read(b)
        
        author_photo_id = Long.read(b)
        
        author = String.read(b)
        
        date = Int.read(b)
        
        blocks = Object.read(b)
        
        caption = Object.read(b)
        
        return PageBlockEmbedPost(url=url, webpage_id=webpage_id, author_photo_id=author_photo_id, author=author, date=date, blocks=blocks, caption=caption)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(String(self.url))
        
        b.write(Long(self.webpage_id))
        
        b.write(Long(self.author_photo_id))
        
        b.write(String(self.author))
        
        b.write(Int(self.date))
        
        b.write(Vector(self.blocks))
        
        b.write(self.caption.write())
        
        return b.getvalue()
