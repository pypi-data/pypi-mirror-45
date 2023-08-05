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


class SendCustomRequest(Object):
    """Attributes:
        ID: ``0xaa2769ed``

    Args:
        custom_method: ``str``
        params: :obj:`DataJSON <DevLGram.api.types.DataJSON>`

    Raises:
        :obj:`RPCError <DevLGram.RPCError>`

    Returns:
        :obj:`DataJSON <DevLGram.api.types.DataJSON>`
    """

    __slots__ = ["custom_method", "params"]

    ID = 0xaa2769ed
    QUALNAME = "bots.SendCustomRequest"

    def __init__(self, *, custom_method: str, params):
        self.custom_method = custom_method  # string
        self.params = params  # DataJSON

    @staticmethod
    def read(b: BytesIO, *args) -> "SendCustomRequest":
        # No flags
        
        custom_method = String.read(b)
        
        params = Object.read(b)
        
        return SendCustomRequest(custom_method=custom_method, params=params)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(String(self.custom_method))
        
        b.write(self.params.write())
        
        return b.getvalue()
