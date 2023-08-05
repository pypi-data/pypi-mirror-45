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


class InputBotInlineMessageGame(Object):
    """Attributes:
        ID: ``0x4b425864``

    Args:
        reply_markup (optional): Either :obj:`ReplyKeyboardHide <DevLGram.api.types.ReplyKeyboardHide>`, :obj:`ReplyKeyboardForceReply <DevLGram.api.types.ReplyKeyboardForceReply>`, :obj:`ReplyKeyboardMarkup <DevLGram.api.types.ReplyKeyboardMarkup>` or :obj:`ReplyInlineMarkup <DevLGram.api.types.ReplyInlineMarkup>`
    """

    __slots__ = ["reply_markup"]

    ID = 0x4b425864
    QUALNAME = "InputBotInlineMessageGame"

    def __init__(self, *, reply_markup=None):
        self.reply_markup = reply_markup  # flags.2?ReplyMarkup

    @staticmethod
    def read(b: BytesIO, *args) -> "InputBotInlineMessageGame":
        flags = Int.read(b)
        
        reply_markup = Object.read(b) if flags & (1 << 2) else None
        
        return InputBotInlineMessageGame(reply_markup=reply_markup)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        flags = 0
        flags |= (1 << 2) if self.reply_markup is not None else 0
        b.write(Int(flags))
        
        if self.reply_markup is not None:
            b.write(self.reply_markup.write())
        
        return b.getvalue()
