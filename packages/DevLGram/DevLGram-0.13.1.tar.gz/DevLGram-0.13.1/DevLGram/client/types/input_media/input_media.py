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

from ..DevLGram_type import DevLGramType


class InputMedia(DevLGramType):
    """This object represents the content of a media message to be sent. It should be one of:

    - :obj:`InputMediaAnimation <DevLGram.InputMediaAnimation>`
    - :obj:`InputMediaDocument <DevLGram.InputMediaDocument>`
    - :obj:`InputMediaAudio <DevLGram.InputMediaAudio>`
    - :obj:`InputMediaPhoto <DevLGram.InputMediaPhoto>`
    - :obj:`InputMediaVideo <DevLGram.InputMediaVideo>`
    """
    __slots__ = ["media", "caption", "parse_mode"]

    def __init__(self, media: str, caption: str, parse_mode: str):
        super().__init__(None)

        self.media = media
        self.caption = caption
        self.parse_mode = parse_mode
