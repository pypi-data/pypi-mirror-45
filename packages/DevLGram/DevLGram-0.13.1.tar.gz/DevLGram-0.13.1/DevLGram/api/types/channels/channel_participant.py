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


class ChannelParticipant(Object):
    """Attributes:
        ID: ``0xd0d9b163``

    Args:
        participant: Either :obj:`ChannelParticipant <DevLGram.api.types.ChannelParticipant>`, :obj:`ChannelParticipantSelf <DevLGram.api.types.ChannelParticipantSelf>`, :obj:`ChannelParticipantCreator <DevLGram.api.types.ChannelParticipantCreator>`, :obj:`ChannelParticipantAdmin <DevLGram.api.types.ChannelParticipantAdmin>` or :obj:`ChannelParticipantBanned <DevLGram.api.types.ChannelParticipantBanned>`
        users: List of either :obj:`UserEmpty <DevLGram.api.types.UserEmpty>` or :obj:`User <DevLGram.api.types.User>`

    See Also:
        This object can be returned by :obj:`channels.GetParticipant <DevLGram.api.functions.channels.GetParticipant>`.
    """

    __slots__ = ["participant", "users"]

    ID = 0xd0d9b163
    QUALNAME = "channels.ChannelParticipant"

    def __init__(self, *, participant, users: list):
        self.participant = participant  # ChannelParticipant
        self.users = users  # Vector<User>

    @staticmethod
    def read(b: BytesIO, *args) -> "ChannelParticipant":
        # No flags
        
        participant = Object.read(b)
        
        users = Object.read(b)
        
        return ChannelParticipant(participant=participant, users=users)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(self.participant.write())
        
        b.write(Vector(self.users))
        
        return b.getvalue()
