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


class ChannelAdminLogEvent(Object):
    """Attributes:
        ID: ``0x3b5a3e40``

    Args:
        id: ``int`` ``64-bit``
        date: ``int`` ``32-bit``
        user_id: ``int`` ``32-bit``
        action: Either :obj:`ChannelAdminLogEventActionChangeTitle <DevLGram.api.types.ChannelAdminLogEventActionChangeTitle>`, :obj:`ChannelAdminLogEventActionChangeAbout <DevLGram.api.types.ChannelAdminLogEventActionChangeAbout>`, :obj:`ChannelAdminLogEventActionChangeUsername <DevLGram.api.types.ChannelAdminLogEventActionChangeUsername>`, :obj:`ChannelAdminLogEventActionChangePhoto <DevLGram.api.types.ChannelAdminLogEventActionChangePhoto>`, :obj:`ChannelAdminLogEventActionToggleInvites <DevLGram.api.types.ChannelAdminLogEventActionToggleInvites>`, :obj:`ChannelAdminLogEventActionToggleSignatures <DevLGram.api.types.ChannelAdminLogEventActionToggleSignatures>`, :obj:`ChannelAdminLogEventActionUpdatePinned <DevLGram.api.types.ChannelAdminLogEventActionUpdatePinned>`, :obj:`ChannelAdminLogEventActionEditMessage <DevLGram.api.types.ChannelAdminLogEventActionEditMessage>`, :obj:`ChannelAdminLogEventActionDeleteMessage <DevLGram.api.types.ChannelAdminLogEventActionDeleteMessage>`, :obj:`ChannelAdminLogEventActionParticipantJoin <DevLGram.api.types.ChannelAdminLogEventActionParticipantJoin>`, :obj:`ChannelAdminLogEventActionParticipantLeave <DevLGram.api.types.ChannelAdminLogEventActionParticipantLeave>`, :obj:`ChannelAdminLogEventActionParticipantInvite <DevLGram.api.types.ChannelAdminLogEventActionParticipantInvite>`, :obj:`ChannelAdminLogEventActionParticipantToggleBan <DevLGram.api.types.ChannelAdminLogEventActionParticipantToggleBan>`, :obj:`ChannelAdminLogEventActionParticipantToggleAdmin <DevLGram.api.types.ChannelAdminLogEventActionParticipantToggleAdmin>`, :obj:`ChannelAdminLogEventActionChangeStickerSet <DevLGram.api.types.ChannelAdminLogEventActionChangeStickerSet>`, :obj:`ChannelAdminLogEventActionTogglePreHistoryHidden <DevLGram.api.types.ChannelAdminLogEventActionTogglePreHistoryHidden>`, :obj:`ChannelAdminLogEventActionDefaultBannedRights <DevLGram.api.types.ChannelAdminLogEventActionDefaultBannedRights>` or :obj:`ChannelAdminLogEventActionStopPoll <DevLGram.api.types.ChannelAdminLogEventActionStopPoll>`
    """

    __slots__ = ["id", "date", "user_id", "action"]

    ID = 0x3b5a3e40
    QUALNAME = "ChannelAdminLogEvent"

    def __init__(self, *, id: int, date: int, user_id: int, action):
        self.id = id  # long
        self.date = date  # int
        self.user_id = user_id  # int
        self.action = action  # ChannelAdminLogEventAction

    @staticmethod
    def read(b: BytesIO, *args) -> "ChannelAdminLogEvent":
        # No flags
        
        id = Long.read(b)
        
        date = Int.read(b)
        
        user_id = Int.read(b)
        
        action = Object.read(b)
        
        return ChannelAdminLogEvent(id=id, date=date, user_id=user_id, action=action)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(Long(self.id))
        
        b.write(Int(self.date))
        
        b.write(Int(self.user_id))
        
        b.write(self.action.write())
        
        return b.getvalue()
