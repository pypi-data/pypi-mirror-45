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


class ImportContacts(Object):
    """Attributes:
        ID: ``0x2c800be5``

    Args:
        contacts: List of :obj:`InputPhoneContact <DevLGram.api.types.InputPhoneContact>`

    Raises:
        :obj:`RPCError <DevLGram.RPCError>`

    Returns:
        :obj:`contacts.ImportedContacts <DevLGram.api.types.contacts.ImportedContacts>`
    """

    __slots__ = ["contacts"]

    ID = 0x2c800be5
    QUALNAME = "contacts.ImportContacts"

    def __init__(self, *, contacts: list):
        self.contacts = contacts  # Vector<InputContact>

    @staticmethod
    def read(b: BytesIO, *args) -> "ImportContacts":
        # No flags
        
        contacts = Object.read(b)
        
        return ImportContacts(contacts=contacts)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(Vector(self.contacts))
        
        return b.getvalue()
