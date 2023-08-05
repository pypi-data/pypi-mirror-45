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


class ChannelAdminLogEventActionParticipantInvite(Object):
    """Attributes:
        ID: ``0xe31c34d8``

    Args:
        participant: Either :obj:`ChannelParticipant <DevLGram.api.types.ChannelParticipant>`, :obj:`ChannelParticipantSelf <DevLGram.api.types.ChannelParticipantSelf>`, :obj:`ChannelParticipantCreator <DevLGram.api.types.ChannelParticipantCreator>`, :obj:`ChannelParticipantAdmin <DevLGram.api.types.ChannelParticipantAdmin>` or :obj:`ChannelParticipantBanned <DevLGram.api.types.ChannelParticipantBanned>`
    """

    __slots__ = ["participant"]

    ID = 0xe31c34d8
    QUALNAME = "ChannelAdminLogEventActionParticipantInvite"

    def __init__(self, *, participant):
        self.participant = participant  # ChannelParticipant

    @staticmethod
    def read(b: BytesIO, *args) -> "ChannelAdminLogEventActionParticipantInvite":
        # No flags
        
        participant = Object.read(b)
        
        return ChannelAdminLogEventActionParticipantInvite(participant=participant)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(self.participant.write())
        
        return b.getvalue()
