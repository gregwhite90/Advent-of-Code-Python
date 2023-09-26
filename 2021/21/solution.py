import re
from typing import List, Dict, NamedTuple, DefaultDict
from collections import defaultdict

from shared import SolutionABC

PLAYER_RE = re.compile(r'Player (?P<id>[1-2]) starting position: (?P<pos>\d+)')

# maps the number of spaces to the number of universes with 3 Dirac Dice rolls
SPACES_OUTCOMES = {
  3: 1,
  4: 3,
  5: 6,
  6: 7,
  7: 6,
  8: 3,
  9: 1,
}

class PlayerStatus(NamedTuple):
  position_idx: int
  score: int

class GameStatus(NamedTuple):
  player_1_status: PlayerStatus
  player_2_status: PlayerStatus

class Solution(SolutionABC):
  def __init__(
    self,
  ):
    self.player_statuses: List[PlayerStatus] = []
    self.cur_player_idx = 0
    self.universes: DefaultDict[GameStatus, int] = defaultdict(int)
    self.universes_won: List[int] = [0, 0]

  def parse_row(
    self,
    row: str,
  ):
    m = PLAYER_RE.match(row)
    assert m
    self.player_statuses.append(PlayerStatus(int(m['pos']) - 1, 0))

  def _setup_game_status(self):
    assert len(self.player_statuses) == 2
    self.universes[GameStatus(*self.player_statuses)] = 1

  def move(self):
    new_universes: DefaultDict[GameStatus, int] = defaultdict(int)
    for game_status, starting_universes in self.universes.items():
      for spaces, universes in SPACES_OUTCOMES.items():
        new_pos = (game_status[self.cur_player_idx].position_idx + spaces) % 10
        new_score = game_status[self.cur_player_idx].score + new_pos + 1
        if new_score >= 21:
          self.universes_won[self.cur_player_idx] += starting_universes * universes
        else:
          new_game_status_list = [*game_status]
          new_game_status_list[self.cur_player_idx] = PlayerStatus(
            new_pos, 
            new_score,
          )
          new_universes[GameStatus(*new_game_status_list)] += starting_universes * universes
    self.universes = new_universes
    self.cur_player_idx = 1 - self.cur_player_idx

  def solve(
    self,
  ) -> int:
    self._setup_game_status()
    while len(self.universes) > 0:
      self.move()
    return max(self.universes_won)