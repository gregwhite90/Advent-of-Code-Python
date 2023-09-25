from typing import Union, NamedTuple, Dict
from enum import Enum, auto
from shared import SolutionABC

class Point(NamedTuple):
  x: int
  y: int

class BlockedReason(Enum):
  ROCK = auto()
  SAND = auto()

class Solution(SolutionABC):
  def __init__(
    self,
  ):
    self._start = Point(500, 0)
    self._max_y = 0
    self._blocked: Dict[Point, BlockedReason] = {}

  def parse_row(
    self,
    row: str,
  ):
    points = [
      Point(*[int(coord) for coord in segment.split(',')])
      for segment in row.split(' -> ')
    ]
    self._max_y = max(points[0].y, self._max_y)
    for i in range(1, len(points)):
      self._max_y = max(points[i].y, self._max_y)
      if points[i - 1].x == points[i].x:
        for y in range(
          min(points[i - 1].y, points[i].y),
          max(points[i - 1].y, points[i].y) + 1,
        ):
          self._blocked[Point(points[i].x, y)] = BlockedReason.ROCK
      else:
        assert points[i - 1].y == points[i].y
        for x in range(
          min(points[i - 1].x, points[i].x),
          max(points[i - 1].x, points[i].x) + 1,
        ):
          self._blocked[Point(x, points[i].y)] = BlockedReason.ROCK

  def _is_blocked(self, point: Point) -> bool:
    return point in self._blocked or point.y >= self._max_y + 2

  def _simulate_sand(
    self,
  ):
    sand = self._start
    while not self._is_blocked(self._start):
      if not self._is_blocked(Point(sand.x, sand.y + 1)):
        sand = Point(sand.x, sand.y + 1)
      elif not self._is_blocked(Point(sand.x - 1, sand.y + 1)):
        sand = Point(sand.x - 1, sand.y + 1)
      elif not self._is_blocked(Point(sand.x + 1, sand.y + 1)):
        sand = Point(sand.x + 1, sand.y + 1)
      else:
        assert sand not in self._blocked
        self._blocked[sand] = BlockedReason.SAND
        sand = self._start

  def _sand_at_rest(self) -> int:
    return sum(
      blocked_reason == BlockedReason.SAND for blocked_reason in self._blocked.values()
    )

  def solve(
    self,
  ) -> Union[int, str]:
    self._simulate_sand()
    return self._sand_at_rest()