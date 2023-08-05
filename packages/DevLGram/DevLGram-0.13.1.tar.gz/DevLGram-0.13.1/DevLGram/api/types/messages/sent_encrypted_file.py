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


class SentEncryptedFile(Object):
    """Attributes:
        ID: ``0x9493ff32``

    Args:
        date: ``int`` ``32-bit``
        file: Either :obj:`EncryptedFileEmpty <DevLGram.api.types.EncryptedFileEmpty>` or :obj:`EncryptedFile <DevLGram.api.types.EncryptedFile>`

    See Also:
        This object can be returned by :obj:`messages.SendEncrypted <DevLGram.api.functions.messages.SendEncrypted>`, :obj:`messages.SendEncryptedFile <DevLGram.api.functions.messages.SendEncryptedFile>` and :obj:`messages.SendEncryptedService <DevLGram.api.functions.messages.SendEncryptedService>`.
    """

    __slots__ = ["date", "file"]

    ID = 0x9493ff32
    QUALNAME = "messages.SentEncryptedFile"

    def __init__(self, *, date: int, file):
        self.date = date  # int
        self.file = file  # EncryptedFile

    @staticmethod
    def read(b: BytesIO, *args) -> "SentEncryptedFile":
        # No flags
        
        date = Int.read(b)
        
        file = Object.read(b)
        
        return SentEncryptedFile(date=date, file=file)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(Int(self.date))
        
        b.write(self.file.write())
        
        return b.getvalue()
