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


class PageBlockAudio(Object):
    """Attributes:
        ID: ``0x804361ea``

    Args:
        audio_id: ``int`` ``64-bit``
        caption: :obj:`PageCaption <DevLGram.api.types.PageCaption>`
    """

    __slots__ = ["audio_id", "caption"]

    ID = 0x804361ea
    QUALNAME = "PageBlockAudio"

    def __init__(self, *, audio_id: int, caption):
        self.audio_id = audio_id  # long
        self.caption = caption  # PageCaption

    @staticmethod
    def read(b: BytesIO, *args) -> "PageBlockAudio":
        # No flags
        
        audio_id = Long.read(b)
        
        caption = Object.read(b)
        
        return PageBlockAudio(audio_id=audio_id, caption=caption)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(Long(self.audio_id))
        
        b.write(self.caption.write())
        
        return b.getvalue()
