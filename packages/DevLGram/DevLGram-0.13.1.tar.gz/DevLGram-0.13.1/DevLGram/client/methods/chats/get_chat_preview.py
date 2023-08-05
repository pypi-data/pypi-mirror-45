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
from DevLGram.api import functions, types
from ...ext import BaseClient


class GetChatPreview(BaseClient):
    def get_chat_preview(
        self,
        invite_link: str
    ):
        """Use this method to get the preview of a chat using the invite link.

        This method only returns a chat preview, if you want to join a chat use :meth:`join_chat`

        Args:
            invite_link (``str``):
                Unique identifier for the target chat in form of *t.me/joinchat/* links.

        Returns:
            Either :obj:`Chat` or :obj:`ChatPreview`, depending on whether you already joined the chat or not.

        Raises:
            :class:`RPCError <DevLGram.RPCError>` in case of a Telegram RPC error.
            ``ValueError`` in case of an invalid invite_link.
        """
        match = self.INVITE_LINK_RE.match(invite_link)

        if match:
            r = self.send(
                functions.messages.CheckChatInvite(
                    hash=match.group(1)
                )
            )

            if isinstance(r, types.ChatInvite):
                return DevLGram.ChatPreview._parse(self, r)

            if isinstance(r, types.ChatInviteAlready):
                chat = r.chat

                if isinstance(chat, types.Chat):
                    return DevLGram.Chat._parse_chat_chat(self, chat)

                if isinstance(chat, types.Channel):
                    return DevLGram.Chat._parse_channel_chat(self, chat)
        else:
            raise ValueError("The invite_link is invalid")
