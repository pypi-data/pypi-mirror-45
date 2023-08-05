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


class MessageMediaWebPage(Object):
    """Attributes:
        ID: ``0xa32dd600``

    Args:
        webpage: Either :obj:`WebPageEmpty <DevLGram.api.types.WebPageEmpty>`, :obj:`WebPagePending <DevLGram.api.types.WebPagePending>`, :obj:`WebPage <DevLGram.api.types.WebPage>` or :obj:`WebPageNotModified <DevLGram.api.types.WebPageNotModified>`

    See Also:
        This object can be returned by :obj:`messages.GetWebPagePreview <DevLGram.api.functions.messages.GetWebPagePreview>` and :obj:`messages.UploadMedia <DevLGram.api.functions.messages.UploadMedia>`.
    """

    __slots__ = ["webpage"]

    ID = 0xa32dd600
    QUALNAME = "MessageMediaWebPage"

    def __init__(self, *, webpage):
        self.webpage = webpage  # WebPage

    @staticmethod
    def read(b: BytesIO, *args) -> "MessageMediaWebPage":
        # No flags
        
        webpage = Object.read(b)
        
        return MessageMediaWebPage(webpage=webpage)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(self.webpage.write())
        
        return b.getvalue()
