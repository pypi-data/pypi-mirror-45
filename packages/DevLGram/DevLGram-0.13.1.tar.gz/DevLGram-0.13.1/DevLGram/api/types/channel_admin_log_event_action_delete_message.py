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


class ChannelAdminLogEventActionDeleteMessage(Object):
    """Attributes:
        ID: ``0x42e047bb``

    Args:
        message: Either :obj:`MessageEmpty <DevLGram.api.types.MessageEmpty>`, :obj:`Message <DevLGram.api.types.Message>` or :obj:`MessageService <DevLGram.api.types.MessageService>`
    """

    __slots__ = ["message"]

    ID = 0x42e047bb
    QUALNAME = "ChannelAdminLogEventActionDeleteMessage"

    def __init__(self, *, message):
        self.message = message  # Message

    @staticmethod
    def read(b: BytesIO, *args) -> "ChannelAdminLogEventActionDeleteMessage":
        # No flags
        
        message = Object.read(b)
        
        return ChannelAdminLogEventActionDeleteMessage(message=message)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(self.message.write())
        
        return b.getvalue()
