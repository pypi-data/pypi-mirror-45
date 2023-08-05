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


class InputPaymentCredentials(Object):
    """Attributes:
        ID: ``0x3417d728``

    Args:
        data: :obj:`DataJSON <DevLGram.api.types.DataJSON>`
        save (optional): ``bool``
    """

    __slots__ = ["data", "save"]

    ID = 0x3417d728
    QUALNAME = "InputPaymentCredentials"

    def __init__(self, *, data, save: bool = None):
        self.save = save  # flags.0?true
        self.data = data  # DataJSON

    @staticmethod
    def read(b: BytesIO, *args) -> "InputPaymentCredentials":
        flags = Int.read(b)
        
        save = True if flags & (1 << 0) else False
        data = Object.read(b)
        
        return InputPaymentCredentials(data=data, save=save)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        flags = 0
        flags |= (1 << 0) if self.save is not None else 0
        b.write(Int(flags))
        
        b.write(self.data.write())
        
        return b.getvalue()
