from enum import Enum
from typing import Union, NamedTuple, Dict, Set

from shared import SolutionABC

class Position(NamedTuple):
  x: int
  y: int

class Status(Enum):
  EAST = '>'
  SOUTH = 'v'
  EMPTY = '.'

class Solution(SolutionABC):
  def __init__(
    self,
  ):
    self.field: Dict[Position, Status] = {}
    self.rows = 0
    self.cols = 0
    self.steps = 0

  def parse_row(
    self,
    row: str,
  ):
    self.cols = len(row)
    for x, char in enumerate(row):
      self.field[Position(x, self.rows)] = Status(char)
    self.rows += 1

  def step(self) -> int:
    """
    Returns the number of sea cucumbers that moved on this step.
    """
    movers = 0
    # east herd moves first
    east_to_move: Set[Position] = set(
      pos for pos, status in self.field.items() if status == Status.EAST and self.field[Position((pos.x + 1) % self.cols, pos.y)] == Status.EMPTY
    )
    for pos in east_to_move:
      self.field[Position((pos.x + 1) % self.cols, pos.y)] = Status.EAST
      self.field[pos] = Status.EMPTY
    movers += len(east_to_move)

    # south herd moves second
    south_to_move: Set[Position] = set(
      pos for pos, status in self.field.items() if status == Status.SOUTH and self.field[Position(pos.x, (pos.y + 1) % self.rows)] == Status.EMPTY
    )
    for pos in south_to_move:
      self.field[Position(pos.x, (pos.y + 1) % self.rows)] = Status.SOUTH
      self.field[pos] = Status.EMPTY
    movers += len(south_to_move)

    self.steps += 1
    return movers

  def solve(
    self,
  ) -> Union[int, str]:
    while True:
      if self.step() == 0:
        break
    return self.steps

  def __str__(self) -> str:
    res = f"After {self.steps} steps:\n\n"
    for y in range(self.rows):
      for x in range(self.cols):
        res += self.field[Position(x, y)].value
      res += '\n'
    return res