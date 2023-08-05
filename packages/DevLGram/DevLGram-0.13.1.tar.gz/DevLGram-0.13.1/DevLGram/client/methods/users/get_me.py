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


class GetMe(BaseClient):
    async def get_me(self) -> "DevLGram.User":
        """A simple method for testing your authorization. Requires no parameters.

        Returns:
            Basic information about the user or bot in form of a :obj:`User` object

        Raises:
            :class:`RPCError <DevLGram.RPCError>` in case of a Telegram RPC error.
        """
        return DevLGram.User._parse(
            self,
            (await self.send(
                functions.users.GetFullUser(
                    id=types.InputPeerSelf()
                )
            )).user
        )
