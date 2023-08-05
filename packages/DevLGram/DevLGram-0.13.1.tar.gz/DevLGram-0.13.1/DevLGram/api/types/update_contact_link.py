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


class UpdateContactLink(Object):
    """Attributes:
        ID: ``0x9d2e67c5``

    Args:
        user_id: ``int`` ``32-bit``
        my_link: Either :obj:`ContactLinkUnknown <DevLGram.api.types.ContactLinkUnknown>`, :obj:`ContactLinkNone <DevLGram.api.types.ContactLinkNone>`, :obj:`ContactLinkHasPhone <DevLGram.api.types.ContactLinkHasPhone>` or :obj:`ContactLinkContact <DevLGram.api.types.ContactLinkContact>`
        foreign_link: Either :obj:`ContactLinkUnknown <DevLGram.api.types.ContactLinkUnknown>`, :obj:`ContactLinkNone <DevLGram.api.types.ContactLinkNone>`, :obj:`ContactLinkHasPhone <DevLGram.api.types.ContactLinkHasPhone>` or :obj:`ContactLinkContact <DevLGram.api.types.ContactLinkContact>`
    """

    __slots__ = ["user_id", "my_link", "foreign_link"]

    ID = 0x9d2e67c5
    QUALNAME = "UpdateContactLink"

    def __init__(self, *, user_id: int, my_link, foreign_link):
        self.user_id = user_id  # int
        self.my_link = my_link  # ContactLink
        self.foreign_link = foreign_link  # ContactLink

    @staticmethod
    def read(b: BytesIO, *args) -> "UpdateContactLink":
        # No flags
        
        user_id = Int.read(b)
        
        my_link = Object.read(b)
        
        foreign_link = Object.read(b)
        
        return UpdateContactLink(user_id=user_id, my_link=my_link, foreign_link=foreign_link)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(Int(self.user_id))
        
        b.write(self.my_link.write())
        
        b.write(self.foreign_link.write())
        
        return b.getvalue()
