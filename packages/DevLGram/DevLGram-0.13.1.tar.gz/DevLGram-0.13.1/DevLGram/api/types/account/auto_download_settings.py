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


class AutoDownloadSettings(Object):
    """Attributes:
        ID: ``0x63cacf26``

    Args:
        low: :obj:`AutoDownloadSettings <DevLGram.api.types.AutoDownloadSettings>`
        medium: :obj:`AutoDownloadSettings <DevLGram.api.types.AutoDownloadSettings>`
        high: :obj:`AutoDownloadSettings <DevLGram.api.types.AutoDownloadSettings>`

    See Also:
        This object can be returned by :obj:`account.GetAutoDownloadSettings <DevLGram.api.functions.account.GetAutoDownloadSettings>`.
    """

    __slots__ = ["low", "medium", "high"]

    ID = 0x63cacf26
    QUALNAME = "account.AutoDownloadSettings"

    def __init__(self, *, low, medium, high):
        self.low = low  # AutoDownloadSettings
        self.medium = medium  # AutoDownloadSettings
        self.high = high  # AutoDownloadSettings

    @staticmethod
    def read(b: BytesIO, *args) -> "AutoDownloadSettings":
        # No flags
        
        low = Object.read(b)
        
        medium = Object.read(b)
        
        high = Object.read(b)
        
        return AutoDownloadSettings(low=low, medium=medium, high=high)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(self.low.write())
        
        b.write(self.medium.write())
        
        b.write(self.high.write())
        
        return b.getvalue()
