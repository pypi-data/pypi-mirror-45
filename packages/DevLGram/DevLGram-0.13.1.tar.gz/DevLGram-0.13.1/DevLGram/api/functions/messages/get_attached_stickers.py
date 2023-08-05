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


class GetAttachedStickers(Object):
    """Attributes:
        ID: ``0xcc5b67cc``

    Args:
        media: Either :obj:`InputStickeredMediaPhoto <DevLGram.api.types.InputStickeredMediaPhoto>` or :obj:`InputStickeredMediaDocument <DevLGram.api.types.InputStickeredMediaDocument>`

    Raises:
        :obj:`RPCError <DevLGram.RPCError>`

    Returns:
        List of either :obj:`StickerSetCovered <DevLGram.api.types.StickerSetCovered>` or :obj:`StickerSetMultiCovered <DevLGram.api.types.StickerSetMultiCovered>`
    """

    __slots__ = ["media"]

    ID = 0xcc5b67cc
    QUALNAME = "messages.GetAttachedStickers"

    def __init__(self, *, media):
        self.media = media  # InputStickeredMedia

    @staticmethod
    def read(b: BytesIO, *args) -> "GetAttachedStickers":
        # No flags
        
        media = Object.read(b)
        
        return GetAttachedStickers(media=media)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(self.media.write())
        
        return b.getvalue()
