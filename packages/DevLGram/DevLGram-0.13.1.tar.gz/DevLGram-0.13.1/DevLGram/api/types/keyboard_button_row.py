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


class KeyboardButtonRow(Object):
    """Attributes:
        ID: ``0x77608b83``

    Args:
        buttons: List of either :obj:`KeyboardButton <DevLGram.api.types.KeyboardButton>`, :obj:`KeyboardButtonUrl <DevLGram.api.types.KeyboardButtonUrl>`, :obj:`KeyboardButtonCallback <DevLGram.api.types.KeyboardButtonCallback>`, :obj:`KeyboardButtonRequestPhone <DevLGram.api.types.KeyboardButtonRequestPhone>`, :obj:`KeyboardButtonRequestGeoLocation <DevLGram.api.types.KeyboardButtonRequestGeoLocation>`, :obj:`KeyboardButtonSwitchInline <DevLGram.api.types.KeyboardButtonSwitchInline>`, :obj:`KeyboardButtonGame <DevLGram.api.types.KeyboardButtonGame>` or :obj:`KeyboardButtonBuy <DevLGram.api.types.KeyboardButtonBuy>`
    """

    __slots__ = ["buttons"]

    ID = 0x77608b83
    QUALNAME = "KeyboardButtonRow"

    def __init__(self, *, buttons: list):
        self.buttons = buttons  # Vector<KeyboardButton>

    @staticmethod
    def read(b: BytesIO, *args) -> "KeyboardButtonRow":
        # No flags
        
        buttons = Object.read(b)
        
        return KeyboardButtonRow(buttons=buttons)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(Vector(self.buttons))
        
        return b.getvalue()
