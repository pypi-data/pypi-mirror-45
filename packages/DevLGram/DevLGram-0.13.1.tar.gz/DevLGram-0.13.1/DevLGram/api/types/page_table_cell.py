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


class PageTableCell(Object):
    """Attributes:
        ID: ``0x34566b6a``

    Args:
        header (optional): ``bool``
        align_center (optional): ``bool``
        align_right (optional): ``bool``
        valign_middle (optional): ``bool``
        valign_bottom (optional): ``bool``
        text (optional): Either :obj:`TextEmpty <DevLGram.api.types.TextEmpty>`, :obj:`TextPlain <DevLGram.api.types.TextPlain>`, :obj:`TextBold <DevLGram.api.types.TextBold>`, :obj:`TextItalic <DevLGram.api.types.TextItalic>`, :obj:`TextUnderline <DevLGram.api.types.TextUnderline>`, :obj:`TextStrike <DevLGram.api.types.TextStrike>`, :obj:`TextFixed <DevLGram.api.types.TextFixed>`, :obj:`TextUrl <DevLGram.api.types.TextUrl>`, :obj:`TextEmail <DevLGram.api.types.TextEmail>`, :obj:`TextConcat <DevLGram.api.types.TextConcat>`, :obj:`TextSubscript <DevLGram.api.types.TextSubscript>`, :obj:`TextSuperscript <DevLGram.api.types.TextSuperscript>`, :obj:`TextMarked <DevLGram.api.types.TextMarked>`, :obj:`TextPhone <DevLGram.api.types.TextPhone>`, :obj:`TextImage <DevLGram.api.types.TextImage>` or :obj:`TextAnchor <DevLGram.api.types.TextAnchor>`
        colspan (optional): ``int`` ``32-bit``
        rowspan (optional): ``int`` ``32-bit``
    """

    __slots__ = ["header", "align_center", "align_right", "valign_middle", "valign_bottom", "text", "colspan", "rowspan"]

    ID = 0x34566b6a
    QUALNAME = "PageTableCell"

    def __init__(self, *, header: bool = None, align_center: bool = None, align_right: bool = None, valign_middle: bool = None, valign_bottom: bool = None, text=None, colspan: int = None, rowspan: int = None):
        self.header = header  # flags.0?true
        self.align_center = align_center  # flags.3?true
        self.align_right = align_right  # flags.4?true
        self.valign_middle = valign_middle  # flags.5?true
        self.valign_bottom = valign_bottom  # flags.6?true
        self.text = text  # flags.7?RichText
        self.colspan = colspan  # flags.1?int
        self.rowspan = rowspan  # flags.2?int

    @staticmethod
    def read(b: BytesIO, *args) -> "PageTableCell":
        flags = Int.read(b)
        
        header = True if flags & (1 << 0) else False
        align_center = True if flags & (1 << 3) else False
        align_right = True if flags & (1 << 4) else False
        valign_middle = True if flags & (1 << 5) else False
        valign_bottom = True if flags & (1 << 6) else False
        text = Object.read(b) if flags & (1 << 7) else None
        
        colspan = Int.read(b) if flags & (1 << 1) else None
        rowspan = Int.read(b) if flags & (1 << 2) else None
        return PageTableCell(header=header, align_center=align_center, align_right=align_right, valign_middle=valign_middle, valign_bottom=valign_bottom, text=text, colspan=colspan, rowspan=rowspan)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        flags = 0
        flags |= (1 << 0) if self.header is not None else 0
        flags |= (1 << 3) if self.align_center is not None else 0
        flags |= (1 << 4) if self.align_right is not None else 0
        flags |= (1 << 5) if self.valign_middle is not None else 0
        flags |= (1 << 6) if self.valign_bottom is not None else 0
        flags |= (1 << 7) if self.text is not None else 0
        flags |= (1 << 1) if self.colspan is not None else 0
        flags |= (1 << 2) if self.rowspan is not None else 0
        b.write(Int(flags))
        
        if self.text is not None:
            b.write(self.text.write())
        
        if self.colspan is not None:
            b.write(Int(self.colspan))
        
        if self.rowspan is not None:
            b.write(Int(self.rowspan))
        
        return b.getvalue()
