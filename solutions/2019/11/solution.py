from collections import defaultdict
from typing import List, NamedTuple, Set, DefaultDict
from enum import Enum

from solutions.shared import SolutionABC, IntcodeComputer, InputMode

class Position(NamedTuple):
  x: int
  y: int

class Color(Enum):
  BLACK = 0
  WHITE = 1

class Direction(Enum):
  UP = 0
  RIGHT = 1
  DOWN = 2
  LEFT = 3

def next_dir(
  direction: Direction,
  output_dir: int, # 0 for left turn or 1 for right turn
) -> Direction:
  return Direction(
    (direction.value + output_dir * 2 - 1) % len(Direction)
  )

def next_pos(
  pos: Position,
  dir: Direction,
) -> Position:
  if dir == Direction.UP:
    return Position(pos.x, pos.y + 1)
  elif dir == Direction.DOWN:
    return Position(pos.x, pos.y - 1)
  elif dir == Direction.LEFT:
    return Position(pos.x - 1, pos.y)
  else:
    assert dir == Direction.RIGHT
    return Position(pos.x + 1, pos.y)

class Solution(SolutionABC):
  def __init__(
    self,
  ):
    self.base_program: List[int] = None
    self.starting_position = Position(0, 0)
    self.colors: DefaultDict[Position, Color] = defaultdict(lambda: Color.BLACK)
    self.colors[self.starting_position] = Color.WHITE
    self.painted: Set[Position] = set()
    self.direction = Direction.UP
    self.min_x = 0
    self.min_y = 0
    self.max_x = 0
    self.max_y = 0

  def parse_row(
    self,
    row: str,
  ):
    self.base_program = [int(val) for val in row.split(',')]

  def paint_hull(
    self,
  ):
    ic = IntcodeComputer(self.base_program, [], [])
    pos = self.starting_position
    while not ic.is_halted():
      ic.enqueue_input(self.colors[pos].value)
      ic.run()
      col, dir = ic.get_outputs()[-2 : ]
      self.colors[pos] = Color(col)
      self.painted.add(pos)
      self.direction = next_dir(self.direction, dir)
      pos = next_pos(pos, self.direction)
      self.min_x = min(self.min_x, pos.x)
      self.max_x = max(self.max_x, pos.x)
      self.min_y = min(self.min_y, pos.y)
      self.max_y = max(self.max_y, pos.y)

  def __str__(self):
    res = ''
    for y in range(self.max_y, self.min_y - 1, -1):
      for x in range(self.min_x, self.max_x + 1):
        res += '#' if self.colors[Position(x, y)] == Color.WHITE else ' '
      res += '\n'
    return res

  def solve(
    self,
  ) -> str:
    self.paint_hull()
    return str(self)