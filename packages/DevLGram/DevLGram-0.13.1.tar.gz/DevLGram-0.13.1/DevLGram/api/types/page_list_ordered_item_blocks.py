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


class PageListOrderedItemBlocks(Object):
    """Attributes:
        ID: ``0x98dd8936``

    Args:
        num: ``str``
        blocks: List of either :obj:`PageBlockUnsupported <DevLGram.api.types.PageBlockUnsupported>`, :obj:`PageBlockTitle <DevLGram.api.types.PageBlockTitle>`, :obj:`PageBlockSubtitle <DevLGram.api.types.PageBlockSubtitle>`, :obj:`PageBlockAuthorDate <DevLGram.api.types.PageBlockAuthorDate>`, :obj:`PageBlockHeader <DevLGram.api.types.PageBlockHeader>`, :obj:`PageBlockSubheader <DevLGram.api.types.PageBlockSubheader>`, :obj:`PageBlockParagraph <DevLGram.api.types.PageBlockParagraph>`, :obj:`PageBlockPreformatted <DevLGram.api.types.PageBlockPreformatted>`, :obj:`PageBlockFooter <DevLGram.api.types.PageBlockFooter>`, :obj:`PageBlockDivider <DevLGram.api.types.PageBlockDivider>`, :obj:`PageBlockAnchor <DevLGram.api.types.PageBlockAnchor>`, :obj:`PageBlockList <DevLGram.api.types.PageBlockList>`, :obj:`PageBlockBlockquote <DevLGram.api.types.PageBlockBlockquote>`, :obj:`PageBlockPullquote <DevLGram.api.types.PageBlockPullquote>`, :obj:`PageBlockPhoto <DevLGram.api.types.PageBlockPhoto>`, :obj:`PageBlockVideo <DevLGram.api.types.PageBlockVideo>`, :obj:`PageBlockCover <DevLGram.api.types.PageBlockCover>`, :obj:`PageBlockEmbed <DevLGram.api.types.PageBlockEmbed>`, :obj:`PageBlockEmbedPost <DevLGram.api.types.PageBlockEmbedPost>`, :obj:`PageBlockCollage <DevLGram.api.types.PageBlockCollage>`, :obj:`PageBlockSlideshow <DevLGram.api.types.PageBlockSlideshow>`, :obj:`PageBlockChannel <DevLGram.api.types.PageBlockChannel>`, :obj:`PageBlockAudio <DevLGram.api.types.PageBlockAudio>`, :obj:`PageBlockKicker <DevLGram.api.types.PageBlockKicker>`, :obj:`PageBlockTable <DevLGram.api.types.PageBlockTable>`, :obj:`PageBlockOrderedList <DevLGram.api.types.PageBlockOrderedList>`, :obj:`PageBlockDetails <DevLGram.api.types.PageBlockDetails>`, :obj:`PageBlockRelatedArticles <DevLGram.api.types.PageBlockRelatedArticles>` or :obj:`PageBlockMap <DevLGram.api.types.PageBlockMap>`
    """

    __slots__ = ["num", "blocks"]

    ID = 0x98dd8936
    QUALNAME = "PageListOrderedItemBlocks"

    def __init__(self, *, num: str, blocks: list):
        self.num = num  # string
        self.blocks = blocks  # Vector<PageBlock>

    @staticmethod
    def read(b: BytesIO, *args) -> "PageListOrderedItemBlocks":
        # No flags
        
        num = String.read(b)
        
        blocks = Object.read(b)
        
        return PageListOrderedItemBlocks(num=num, blocks=blocks)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(String(self.num))
        
        b.write(Vector(self.blocks))
        
        return b.getvalue()
