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


class PageBlockRelatedArticles(Object):
    """Attributes:
        ID: ``0x16115a96``

    Args:
        title: Either :obj:`TextEmpty <DevLGram.api.types.TextEmpty>`, :obj:`TextPlain <DevLGram.api.types.TextPlain>`, :obj:`TextBold <DevLGram.api.types.TextBold>`, :obj:`TextItalic <DevLGram.api.types.TextItalic>`, :obj:`TextUnderline <DevLGram.api.types.TextUnderline>`, :obj:`TextStrike <DevLGram.api.types.TextStrike>`, :obj:`TextFixed <DevLGram.api.types.TextFixed>`, :obj:`TextUrl <DevLGram.api.types.TextUrl>`, :obj:`TextEmail <DevLGram.api.types.TextEmail>`, :obj:`TextConcat <DevLGram.api.types.TextConcat>`, :obj:`TextSubscript <DevLGram.api.types.TextSubscript>`, :obj:`TextSuperscript <DevLGram.api.types.TextSuperscript>`, :obj:`TextMarked <DevLGram.api.types.TextMarked>`, :obj:`TextPhone <DevLGram.api.types.TextPhone>`, :obj:`TextImage <DevLGram.api.types.TextImage>` or :obj:`TextAnchor <DevLGram.api.types.TextAnchor>`
        articles: List of :obj:`PageRelatedArticle <DevLGram.api.types.PageRelatedArticle>`
    """

    __slots__ = ["title", "articles"]

    ID = 0x16115a96
    QUALNAME = "PageBlockRelatedArticles"

    def __init__(self, *, title, articles: list):
        self.title = title  # RichText
        self.articles = articles  # Vector<PageRelatedArticle>

    @staticmethod
    def read(b: BytesIO, *args) -> "PageBlockRelatedArticles":
        # No flags
        
        title = Object.read(b)
        
        articles = Object.read(b)
        
        return PageBlockRelatedArticles(title=title, articles=articles)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(self.title.write())
        
        b.write(Vector(self.articles))
        
        return b.getvalue()
