import itertools
from enum import Enum
from typing import NamedTuple, Dict, Set

from shared import SolutionABC

class Status(Enum):
  ACTIVE = '#'
  INACTIVE = '.'

class Point(NamedTuple):
  x: int
  y: int
  z: int
  w: int

class BoundingBox(NamedTuple):
  min_x: int
  min_y: int
  min_z: int
  min_w: int
  max_x: int
  max_y: int
  max_z: int
  max_w: int

def neighbors(point: Point) -> Set[Point]:
  res = set(Point(*coords) for coords in itertools.product(
    range(point.x - 1, point.x + 2),
    range(point.y - 1, point.y + 2),
    range(point.z - 1, point.z + 2),
    range(point.w - 1, point.w + 2),
  ))
  res.remove(point)
  return res

def all_points(bounding_box: BoundingBox) -> Set[Point]:
  return set(Point(*coords) for coords in itertools.product(
    range(bounding_box.min_x, bounding_box.max_x + 1),
    range(bounding_box.min_y, bounding_box.max_y + 1),
    range(bounding_box.min_z, bounding_box.max_z + 1),
    range(bounding_box.min_w, bounding_box.max_w + 1),
  ))
  
class Solution(SolutionABC):
  def __init__(
    self,
  ):
    self.cubes: Dict[Point, Status] = {}
    self.bounding_box: BoundingBox = None

  def parse_row(
    self,
    row: str,
  ):
    if self.bounding_box is None:
      self.bounding_box = BoundingBox(
        0,
        0,
        0,
        0,
        len(row) - 1,
        0,
        0,
        0,
      )
    else:
      self.bounding_box = BoundingBox(
        0,
        0,
        0,
        0,
        max(len(row) - 1, self.bounding_box.max_x),
        self.bounding_box.max_y + 1,
        0,
        0,
      )
    for x, char in enumerate(row):
      self.cubes[Point(x, self.bounding_box.max_y, 0, 0)] = Status(char)

  def cycle(self):
    self.bounding_box = BoundingBox(
      self.bounding_box.min_x - 1,
      self.bounding_box.min_y - 1,
      self.bounding_box.min_z - 1,
      self.bounding_box.min_w - 1,
      self.bounding_box.max_x + 1,
      self.bounding_box.max_y + 1,
      self.bounding_box.max_z + 1,
      self.bounding_box.max_w + 1,
    )
    new_cubes: Dict[Point, Status] = {}
    for point in all_points(self.bounding_box):
      adj_active = sum(1 if adj in self.cubes and self.cubes[adj] == Status.ACTIVE else 0 for adj in neighbors(point))
      if point in self.cubes and self.cubes[point] == Status.ACTIVE:
        if adj_active == 2 or adj_active == 3:
          new_cubes[point] = Status.ACTIVE
        else:
          new_cubes[point] = Status.INACTIVE
      else:
        if adj_active == 3:
          new_cubes[point] = Status.ACTIVE
        else:
          new_cubes[point] = Status.INACTIVE
    self.cubes = new_cubes

  def num_active(self) -> int:
    return sum(status == Status.ACTIVE for status in self.cubes.values())
      
  def solve(
    self,
  ) -> int:
    for _ in range(6):
      self.cycle()
    return self.num_active()