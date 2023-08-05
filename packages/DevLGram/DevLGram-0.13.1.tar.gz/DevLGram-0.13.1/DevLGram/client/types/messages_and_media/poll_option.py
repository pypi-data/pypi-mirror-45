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
from ..DevLGram_type import DevLGramType


class PollOption(DevLGramType):
    """This object represents a Poll Option.

    Args:
        text (``str``):
            Text of the poll option.

        voters (``int``):
            The number of users who voted this option.
            It will be 0 until you vote for the poll.

        data (``bytes``):
            Unique data that identifies this option among all the other options in a poll.
    """

    __slots__ = ["text", "voters", "data"]

    def __init__(
        self,
        *,
        client: "DevLGram.client.ext.BaseClient",
        text: str,
        voters: int,
        data: bytes
    ):
        super().__init__(client)

        self.text = text
        self.voters = voters
        self.data = data
