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


class AnswerWebhookJSONQuery(Object):
    """Attributes:
        ID: ``0xe6213f4d``

    Args:
        query_id: ``int`` ``64-bit``
        data: :obj:`DataJSON <DevLGram.api.types.DataJSON>`

    Raises:
        :obj:`RPCError <DevLGram.RPCError>`

    Returns:
        ``bool``
    """

    __slots__ = ["query_id", "data"]

    ID = 0xe6213f4d
    QUALNAME = "bots.AnswerWebhookJSONQuery"

    def __init__(self, *, query_id: int, data):
        self.query_id = query_id  # long
        self.data = data  # DataJSON

    @staticmethod
    def read(b: BytesIO, *args) -> "AnswerWebhookJSONQuery":
        # No flags
        
        query_id = Long.read(b)
        
        data = Object.read(b)
        
        return AnswerWebhookJSONQuery(query_id=query_id, data=data)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(Long(self.query_id))
        
        b.write(self.data.write())
        
        return b.getvalue()
