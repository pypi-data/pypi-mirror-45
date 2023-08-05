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

from typing import Tuple

import DevLGram
from DevLGram.client.filters.filter import Filter
from DevLGram.client.handlers.handler import Handler
from ...ext import BaseClient


class OnMessage(BaseClient):
    def on_message(
        self=None,
        filters=None,
        group: int = 0
    ) -> callable:
        """Use this decorator to automatically register a function for handling messages.
        This does the same thing as :meth:`add_handler` using the :class:`MessageHandler`.

        Args:
            filters (:obj:`Filters <DevLGram.Filters>`):
                Pass one or more filters to allow only a subset of messages to be passed
                in your function.

            group (``int``, *optional*):
                The group identifier, defaults to 0.
        """

        def decorator(func: callable) -> Tuple[Handler, int]:
            if isinstance(func, tuple):
                func = func[0].callback

            handler = DevLGram.MessageHandler(func, filters)

            if isinstance(self, Filter):
                return DevLGram.MessageHandler(func, self), group if filters is None else filters

            if self is not None:
                self.add_handler(handler, group)

            return handler, group

        return decorator
