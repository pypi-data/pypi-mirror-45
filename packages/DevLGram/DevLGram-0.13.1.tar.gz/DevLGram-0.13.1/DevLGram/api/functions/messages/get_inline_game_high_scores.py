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


class GetInlineGameHighScores(Object):
    """Attributes:
        ID: ``0x0f635e1b``

    Args:
        id: :obj:`InputBotInlineMessageID <DevLGram.api.types.InputBotInlineMessageID>`
        user_id: Either :obj:`InputUserEmpty <DevLGram.api.types.InputUserEmpty>`, :obj:`InputUserSelf <DevLGram.api.types.InputUserSelf>` or :obj:`InputUser <DevLGram.api.types.InputUser>`

    Raises:
        :obj:`RPCError <DevLGram.RPCError>`

    Returns:
        :obj:`messages.HighScores <DevLGram.api.types.messages.HighScores>`
    """

    __slots__ = ["id", "user_id"]

    ID = 0x0f635e1b
    QUALNAME = "messages.GetInlineGameHighScores"

    def __init__(self, *, id, user_id):
        self.id = id  # InputBotInlineMessageID
        self.user_id = user_id  # InputUser

    @staticmethod
    def read(b: BytesIO, *args) -> "GetInlineGameHighScores":
        # No flags
        
        id = Object.read(b)
        
        user_id = Object.read(b)
        
        return GetInlineGameHighScores(id=id, user_id=user_id)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(self.id.write())
        
        b.write(self.user_id.write())
        
        return b.getvalue()
