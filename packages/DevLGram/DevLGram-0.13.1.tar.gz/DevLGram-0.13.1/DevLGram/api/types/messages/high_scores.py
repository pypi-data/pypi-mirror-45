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


class HighScores(Object):
    """Attributes:
        ID: ``0x9a3bfd99``

    Args:
        scores: List of :obj:`HighScore <DevLGram.api.types.HighScore>`
        users: List of either :obj:`UserEmpty <DevLGram.api.types.UserEmpty>` or :obj:`User <DevLGram.api.types.User>`

    See Also:
        This object can be returned by :obj:`messages.GetGameHighScores <DevLGram.api.functions.messages.GetGameHighScores>` and :obj:`messages.GetInlineGameHighScores <DevLGram.api.functions.messages.GetInlineGameHighScores>`.
    """

    __slots__ = ["scores", "users"]

    ID = 0x9a3bfd99
    QUALNAME = "messages.HighScores"

    def __init__(self, *, scores: list, users: list):
        self.scores = scores  # Vector<HighScore>
        self.users = users  # Vector<User>

    @staticmethod
    def read(b: BytesIO, *args) -> "HighScores":
        # No flags
        
        scores = Object.read(b)
        
        users = Object.read(b)
        
        return HighScores(scores=scores, users=users)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(Vector(self.scores))
        
        b.write(Vector(self.users))
        
        return b.getvalue()
