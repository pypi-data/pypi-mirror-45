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

from typing import List

from DevLGram.api import functions, types
from DevLGram.errors import PeerIdInvalid
from ...ext import BaseClient


class DeleteContacts(BaseClient):
    async def delete_contacts(
        self,
        ids: List[int]
    ):
        """Use this method to delete contacts from your Telegram address book.

        Args:
            ids (List of ``int``):
                A list of unique identifiers for the target users.
                Can be an ID (int), a username (string) or phone number (string).

        Returns:
            True on success.

        Raises:
            :class:`RPCError <DevLGram.RPCError>` in case of a Telegram RPC error.
        """
        contacts = []

        for i in ids:
            try:
                input_user = await self.resolve_peer(i)
            except PeerIdInvalid:
                continue
            else:
                if isinstance(input_user, types.InputPeerUser):
                    contacts.append(input_user)

        return await self.send(
            functions.contacts.DeleteContacts(
                id=contacts
            )
        )
