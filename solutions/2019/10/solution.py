import math
from typing import NamedTuple, Set, Dict

from solutions.shared import SolutionABC

class Location(NamedTuple):
  x: int
  y: int

class Direction(NamedTuple):
  delta_x: int
  delta_y: int

class Vector(NamedTuple):
  dir: Direction
  dist: int

def direction(
  origin: Location,
  dest: Location,
) -> Direction:
  delta_x = dest.x - origin.x
  delta_y = dest.y - origin.y
  if delta_x == 0 and delta_y == 0:
    return Direction(0, 0)
  elif delta_x == 0:
    return Direction(0, delta_y // abs(delta_y))
  elif delta_y == 0:
    return Direction(delta_x // abs(delta_x), 0)
  else:
    gcd = math.gcd(delta_x, delta_y)
    return Direction(delta_x // gcd, delta_y // gcd)

def distance(
  origin: Location,
  dest: Location,
) -> int:
  return abs(dest.x - origin.x) + abs(dest.y - origin.y)

def vector(
  origin: Location,
  dest: Location,
) -> Vector:
  return Vector(direction(origin, dest), distance(origin, dest))

class Solution(SolutionABC):
  def __init__(
    self,
  ):
    self.asteroids: Set[Location] = set()
    self.rows = 0
    self.cols = 0
    self.monitoring_station: Location = None
    self.ms_visible: Dict[Direction, Location] = {}

  def parse_row(
    self,
    row: str,
  ):
    if self.cols > 0:
      assert self.cols == len(row)
    else:
      self.cols = len(row)
    for i, char in enumerate(row):
      if char == '#':
        self.asteroids.add(Location(i, self.rows))
    self.rows += 1

  def visible_asteroids(
    self,
    origin: Location,
  ) -> Dict[Direction, Location]:
    visible: Dict[Direction, Location] = {}
    for dest in self.asteroids:
      if dest == origin: continue
      vec = vector(origin, dest)
      if vec.dir not in visible or vec.dist < distance(origin, visible[vec.dir]):
        visible[vec.dir] = dest
    return visible

  def calculate_monitoring_station(
    self,
  ):
    for asteroid in self.asteroids:
      visible = self.visible_asteroids(asteroid)
      if len(visible) > len(self.ms_visible):
        self.ms_visible = visible
        self.monitoring_station = asteroid

  def adj_atan2(
    self,
    locn: Location,
  ) -> float:
    assert self.monitoring_station is not None
    at2 = math.atan2(locn.x - self.monitoring_station.x, self.monitoring_station.y - locn.y)
    if at2 < 0: return 2 * math.pi + at2
    else: return at2

  def nth_vaporized_asteroid(
    self,
    n: int,
  ) -> Location:
    assert self.monitoring_station is not None
    assert len(self.ms_visible) >= n
    visible_list = list(self.ms_visible.values())
    visible_list.sort(key=self.adj_atan2)
    return visible_list[n - 1]

  def output(
    self,
    n: int = 200,
  ) -> int:
    nth_vaporized_asteroid = self.nth_vaporized_asteroid(n)
    return 100 * nth_vaporized_asteroid.x + nth_vaporized_asteroid.y
    
  def solve(
    self,
  ) -> int:
    self.calculate_monitoring_station()
    return self.output()