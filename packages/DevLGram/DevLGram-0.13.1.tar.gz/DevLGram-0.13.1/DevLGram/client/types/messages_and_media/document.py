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

from struct import pack

import DevLGram
from DevLGram.api import types
from .photo_size import PhotoSize
from ..DevLGram_type import DevLGramType
from ...ext.utils import encode


class Document(DevLGramType):
    """This object represents a general file (as opposed to photos, voice messages, audio files, ...).

    Args:
        file_id (``str``):
            Unique file identifier.

        thumb (:obj:`PhotoSize <DevLGram.PhotoSize>`, *optional*):
            Document thumbnail as defined by sender.

        file_name (``str``, *optional*):
            Original filename as defined by sender.

        mime_type (``str``, *optional*):
            MIME type of the file as defined by sender.

        file_size (``int``, *optional*):
            File size.

        date (``int``, *optional*):
            Date the document was sent in Unix time.
    """

    __slots__ = ["file_id", "thumb", "file_name", "mime_type", "file_size", "date"]

    def __init__(
        self,
        *,
        client: "DevLGram.client.ext.BaseClient",
        file_id: str,
        thumb: PhotoSize = None,
        file_name: str = None,
        mime_type: str = None,
        file_size: int = None,
        date: int = None
    ):
        super().__init__(client)

        self.file_id = file_id
        self.thumb = thumb
        self.file_name = file_name
        self.mime_type = mime_type
        self.file_size = file_size
        self.date = date

    @staticmethod
    def _parse(client, document: types.Document, file_name: str) -> "Document":
        return Document(
            file_id=encode(
                pack(
                    "<iiqq",
                    5,
                    document.dc_id,
                    document.id,
                    document.access_hash
                )
            ),
            thumb=PhotoSize._parse(client, document.thumbs),
            file_name=file_name,
            mime_type=document.mime_type,
            file_size=document.size,
            date=document.date,
            client=client
        )
