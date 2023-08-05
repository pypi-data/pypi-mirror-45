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

import DevLGram
from DevLGram.api import types
from DevLGram.client.types.DevLGram_type import DevLGramType
from .game_high_score import GameHighScore


class GameHighScores(DevLGramType):
    """This object represents the high scores table for a game.

    Args:
        total_count (``int``):
            Total number of scores the target game has.

        game_high_scores (List of :obj:`GameHighScore <DevLGram.GameHighScore>`):
            Game scores.
    """

    __slots__ = ["total_count", "game_high_scores"]

    def __init__(
        self,
        *,
        client: "DevLGram.client.ext.BaseClient",
        total_count: int,
        game_high_scores: List[GameHighScore]
    ):
        super().__init__(client)

        self.total_count = total_count
        self.game_high_scores = game_high_scores

    @staticmethod
    def _parse(client, game_high_scores: types.messages.HighScores) -> "GameHighScores":
        return GameHighScores(
            total_count=len(game_high_scores.scores),
            game_high_scores=[
                GameHighScore._parse(client, score, game_high_scores.users)
                for score in game_high_scores.scores],
            client=client
        )
