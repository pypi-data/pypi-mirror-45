# DevLGram - Telegram MTProto API Client Library for Python
# Copyright (C) 2017-2018 Dan Tès <https://github.com/devladityanugraha>
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

from ..DevLGram_type import DevLGramType

"""- :obj:`InputLocationMessageContent`
    - :obj:`InputVenueMessageContent`
    - :obj:`InputContactMessageContent`"""


class InputMessageContent(DevLGramType):
    """This object represents the content of a message to be sent as a result of an inline query.

    DevLGram currently supports the following 4 types:

    - :obj:`InputTextMessageContent`
    """

    __slots__ = []

    def __init__(self):
        super().__init__(None)
