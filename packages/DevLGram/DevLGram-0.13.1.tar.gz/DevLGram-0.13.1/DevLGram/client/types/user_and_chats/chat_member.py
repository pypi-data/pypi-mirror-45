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

import DevLGram

from DevLGram.api import types
from ..DevLGram_type import DevLGramType


class ChatMember(DevLGramType):
    """This object contains information about one member of a chat.

    Args:
        user (:obj:`User <DevLGram.User>`):
            Information about the user.

        status (``str``):
            The member's status in the chat.
            Can be "creator", "administrator", "member", "restricted", "left" or "kicked".

        date (``int``, *optional*):
            Date when the user joined, unix time. Not available for creator.

        invited_by (:obj:`User <DevLGram.User>`, *optional*):
            Administrators and self member only. Information about the user who invited this member.
            In case the user joined by himself this will be the same as "user".

        promoted_by (:obj:`User <DevLGram.User>`, *optional*):
            Administrators only. Information about the user who promoted this member as administrator.

        restricted_by (:obj:`User <DevLGram.User>`, *optional*):
            Restricted and kicked only. Information about the user who restricted or kicked this member.

        permissions (:obj:`ChatPermissions <DevLGram.ChatPermissions>` *optional*):
            Administrators, restricted and kicked members only.
            Information about the member permissions.
    """

    __slots__ = ["user", "status", "date", "invited_by", "promoted_by", "restricted_by", "permissions"]

    def __init__(
        self,
        *,
        client: "DevLGram.client.ext.BaseClient",
        user: "DevLGram.User",
        status: str,
        date: int = None,
        invited_by: "DevLGram.User" = None,
        promoted_by: "DevLGram.User" = None,
        restricted_by: "DevLGram.User" = None,
        permissions: "DevLGram.ChatPermissions" = None
    ):
        super().__init__(client)

        self.user = user
        self.status = status
        self.date = date
        self.invited_by = invited_by
        self.promoted_by = promoted_by
        self.restricted_by = restricted_by
        self.permissions = permissions

    @staticmethod
    def _parse(client, member, users) -> "ChatMember":
        user = DevLGram.User._parse(client, users[member.user_id])

        invited_by = (
            DevLGram.User._parse(client, users[member.inviter_id])
            if getattr(member, "inviter_id", None) else None
        )

        if isinstance(member, (types.ChannelParticipant, types.ChannelParticipantSelf, types.ChatParticipant)):
            return ChatMember(
                user=user,
                status="member",
                date=member.date,
                invited_by=invited_by,
                client=client
            )

        if isinstance(member, (types.ChannelParticipantCreator, types.ChatParticipantCreator)):
            return ChatMember(
                user=user,
                status="creator",
                client=client
            )

        if isinstance(member, types.ChatParticipantAdmin):
            return ChatMember(
                user=user,
                status="administrator",
                date=member.date,
                invited_by=invited_by,
                client=client
            )

        if isinstance(member, types.ChannelParticipantAdmin):
            return ChatMember(
                user=user,
                status="administrator",
                date=member.date,
                invited_by=invited_by,
                promoted_by=DevLGram.User._parse(client, users[member.promoted_by]),
                permissions=DevLGram.ChatPermissions._parse(member),
                client=client
            )

        if isinstance(member, types.ChannelParticipantBanned):
            return ChatMember(
                user=user,
                status=(
                    "kicked" if member.banned_rights.view_messages
                    else "left" if member.left
                    else "restricted"
                ),
                date=member.date,
                restricted_by=DevLGram.User._parse(client, users[member.kicked_by]),
                permissions=DevLGram.ChatPermissions._parse(member),
                client=client
            )
