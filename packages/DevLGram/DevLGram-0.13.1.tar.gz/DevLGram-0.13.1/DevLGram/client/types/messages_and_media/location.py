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


class Location(DevLGramType):
    """This object represents a point on the map.

    Args:
        longitude (``float``):
            Longitude as defined by sender.

        latitude (``float``):
            Latitude as defined by sender.
    """

    __slots__ = ["longitude", "latitude"]

    def __init__(
        self,
        *,
        client: "DevLGram.client.ext.BaseClient",
        longitude: float,
        latitude: float
    ):
        super().__init__(client)

        self.longitude = longitude
        self.latitude = latitude

    @staticmethod
    def _parse(client, geo_point: types.GeoPoint) -> "Location":
        if isinstance(geo_point, types.GeoPoint):
            return Location(
                longitude=geo_point.long,
                latitude=geo_point.lat,
                client=client
            )
