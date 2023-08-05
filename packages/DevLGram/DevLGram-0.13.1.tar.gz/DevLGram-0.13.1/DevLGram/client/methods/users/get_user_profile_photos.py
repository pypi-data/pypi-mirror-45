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

from typing import Union

import DevLGram
from DevLGram.api import functions
from ...ext import BaseClient


class GetUserProfilePhotos(BaseClient):
    async def get_user_profile_photos(
        self,
        user_id: Union[int, str],
        offset: int = 0,
        limit: int = 100
    ) -> "DevLGram.UserProfilePhotos":
        """Use this method to get a list of profile pictures for a user.

        Args:
            user_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target chat.
                For your personal cloud (Saved Messages) you can simply use "me" or "self".
                For a contact that exists in your Telegram address book you can use his phone number (str).

            offset (``int``, *optional*):
                Sequential number of the first photo to be returned.
                By default, all photos are returned.

            limit (``int``, *optional*):
                Limits the number of photos to be retrieved.
                Values between 1—100 are accepted. Defaults to 100.

        Returns:
            On success, a :obj:`UserProfilePhotos` object is returned.

        Raises:
            :class:`RPCError <DevLGram.RPCError>` in case of a Telegram RPC error.
        """
        return DevLGram.UserProfilePhotos._parse(
            self,
            await self.send(
                functions.photos.GetUserPhotos(
                    user_id=await self.resolve_peer(user_id),
                    offset=offset,
                    max_id=0,
                    limit=limit
                )
            )
        )
