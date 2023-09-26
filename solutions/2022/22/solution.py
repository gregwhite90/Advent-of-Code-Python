import re
from typing import Dict, NamedTuple
from enum import Enum

from solutions.shared import SolutionABC

BOARD_RE = re.compile(r'[\ \.\#]+')
INSTRUCTIONS_RE = re.compile(r'([LR])')

class Point(NamedTuple):
  x: int
  y: int

class TileType(Enum):
  OPEN = '.'
  WALL = '#'

class Facing(Enum):
  RIGHT = 0
  DOWN = 1
  LEFT = 2
  UP = 3

class Orientation(NamedTuple):
  point: Point
  facing: Facing

class Solution(SolutionABC):
  def __init__(
    self,
  ):
    self._board: Dict[Point, TileType] = {}
    self._rows = 0
    self._start: Point = None
    self._borders: Dict[Orientation, Orientation] = {}

  def parse_row(
    self,
    row: str,
  ):
    if len(row) >= 0:
      if BOARD_RE.match(row):
        self._parse_board_row(row)        
      else:
        self._set_borders()
        self._parse_instructions_row(row)

  def _parse_board_row(self, row: str):
    for col, char in enumerate(row):
      if self._start is None and self._rows == 0 and char != ' ':
        self._start = Point(col, self._rows)
      if char != ' ':
        self._board[Point(col, self._rows)] = TileType(char)
    self._rows += 1

  def _parse_instructions_row(
    self,
    row: str,
  ):
    self._instructions = INSTRUCTIONS_RE.split(row)

  def _set_borders(self):
    # 50x50 cube sides are referenced here starting from top left, then across and then down
    # 0 <-> 1, 0 <-> 2, 2 <-> 4, 3 <-> 4, 3 <-> 5 all not required, they will act as expected without knowing about a border.
    for i in range(50):
      # 1 <-> 2. confirmed
      self._borders[Orientation(Point(100 + i, 49), Facing.DOWN)] = Orientation(Point(99, 50 + i), Facing.LEFT)
      self._borders[Orientation(Point(99, 50 + i), Facing.RIGHT)] = Orientation(Point(100 + i, 49), Facing.UP)
      # 1 <-> 4. confirmed (changed)
      self._borders[Orientation(Point(149, i), Facing.RIGHT)] = Orientation(Point(99, 149 - i), Facing.LEFT)
      self._borders[Orientation(Point(99, 149 - i), Facing.RIGHT)] = Orientation(Point(149, i), Facing.LEFT)
      # 1 <-> 5. confirmed
      self._borders[Orientation(Point(100 + i, 0), Facing.UP)] = Orientation(Point(i, 199), Facing.UP)
      self._borders[Orientation(Point(i, 199), Facing.DOWN)] = Orientation(Point(100 + i, 0), Facing.DOWN)
      # 0 <-> 3. confirmed
      self._borders[Orientation(Point(50, i), Facing.LEFT)] = Orientation(Point(0, 149 - i), Facing.RIGHT)
      self._borders[Orientation(Point(0, 149 - i), Facing.LEFT)] = Orientation(Point(50, i), Facing.RIGHT)
      # 0 <-> 5. confirmed (changed)
      self._borders[Orientation(Point(50 + i, 0), Facing.UP)] = Orientation(Point(0, 150 + i), Facing.RIGHT)
      self._borders[Orientation(Point(0, 150 + i), Facing.LEFT)] = Orientation(Point(50 + i, 0), Facing.DOWN)
      # 2 <-> 3. confirmed
      self._borders[Orientation(Point(50, 50 + i), Facing.LEFT)] = Orientation(Point(i, 100), Facing.DOWN)
      self._borders[Orientation(Point(i, 100), Facing.UP)] = Orientation(Point(50, 50 + i), Facing.RIGHT) 
      # 4 <-> 5. confirmed
      self._borders[Orientation(Point(50 + i, 149), Facing.DOWN)] = Orientation(Point(49, 150 + i), Facing.LEFT) 
      self._borders[Orientation(Point(49, 150 + i), Facing.RIGHT)] = Orientation(Point(50 + i, 149), Facing.UP)
      
  def _next_board_tile(
    self,
    orientation: Orientation,
  ) -> TileType:
    next_o = self._next_orientation(orientation)
    return self._board[next_o.point]

  def _next_orientation(
    self,
    orientation: Orientation,
  ) -> Orientation:
    if orientation in self._borders:
      return self._borders[orientation]
    if orientation.facing == Facing.RIGHT:
      next_pt = Point(orientation.point.x + 1, orientation.point.y)
    elif orientation.facing == Facing.LEFT:
      next_pt = Point(orientation.point.x - 1, orientation.point.y)
    elif orientation.facing == Facing.DOWN:
      next_pt = Point(orientation.point.x, orientation.point.y + 1)
    else:
      assert orientation.facing == Facing.UP
      next_pt = Point(orientation.point.x, orientation.point.y - 1)
    return Orientation(next_pt, orientation.facing)

  def _take_n_steps(
    self,
    orientation: Orientation,
    n: int,
  ) -> Orientation:
    steps_taken = 0
    while steps_taken < n:
      if self._next_board_tile(orientation) == TileType.WALL:
        break
      else:
        assert self._next_board_tile(orientation) == TileType.OPEN
        orientation = self._next_orientation(orientation)
        steps_taken += 1
    return orientation

  def _turn(self, orientation: Orientation, direction: str) -> Orientation:
    if direction == 'L':
      return Orientation(
        orientation.point,
        Facing((orientation.facing.value - 1) % len(Facing)),
      )
    else:
      assert direction == 'R'
      return Orientation(
        orientation.point,
        Facing((orientation.facing.value + 1) % len(Facing)),
      )    
    
  def solve(
    self,
  ) -> int:
    return self._password(self._follow_all_instructions())

  def _follow_all_instructions(self) -> Orientation:
    orientation = Orientation(
      self._start,
      Facing.RIGHT,
    )
    for instruction in self._instructions:
      if instruction == 'L' or instruction == 'R':
        orientation = self._turn(orientation, instruction)
      else:
        orientation = self._take_n_steps(orientation, int(instruction))
    return orientation

  def _password(self, orientation: Orientation) -> int:
    return 1000 * (orientation.point.y + 1) + 4 * (orientation.point.x + 1) + orientation.facing.value
    