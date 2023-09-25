from __future__ import annotations
import heapq
import itertools
from typing import Dict, NamedTuple, Set, List

class Point(NamedTuple):
  x: int
  y: int

counter = itertools.count()

class Path:
  def __init__(
    self,
    heightmap: Heightmap,
    steps: int,
    point: Point,
    visited: Set[Point],
  ):
    self.heightmap = heightmap
    self.steps = steps
    self.point = point
    self.visited = visited
    self.counter: int = next(counter)

  def __lt__(self, other: Path):
    assert self.heightmap is other.heightmap
    if self.steps != other.steps:
      return self.steps < other.steps
    elif self.heightmap.height(self.point) != self.heightmap.height(other.point):
      return self.heightmap.height(self.point) < self.heightmap.height(other.point)
    else:
      return self.counter < other.counter

class Heightmap:
  def __init__(self):
    self._heightmap: Dict[Point, int] = {}
    self._start: Point = None
    self._end: Point = None
    self._cols = 0
    self._rows = 0
    self._fewest_steps_to_reach: Dict[Point, int] = {}


  def _reachable_points(self, point: Point) -> Set[Point]:
    adj = set()
    if point.x != 0: adj.add(Point(point.x - 1, point.y))
    if point.y != 0: adj.add(Point(point.x, point.y - 1))
    if point.x != self._cols - 1: adj.add(Point(point.x + 1, point.y))
    if point.y != self._rows - 1: adj.add(Point(point.x, point.y + 1))
    for pt in list(adj):
      if self._heightmap[pt] < self._heightmap[point] - 1:
        adj.remove(pt)
    return adj

  def height(self, point: Point) -> int:
    return self._heightmap[point]

  def distance_from_end(self, point: Point) -> int:
    return abs(point.x - self._end.x) + abs(point.y - self._end.y)
    
  def add_row(self, row: str):
    baseline_height = ord('a')
    if self._cols > 0:
      assert len(row) == self._cols
    else:
      self._cols = len(row)
    for x, height_char in enumerate(row):
      pt = Point(x, self._rows)
      if height_char == 'S':
        self._start = pt
        self._heightmap[pt] = ord('a') - baseline_height
      elif height_char == 'E':
        self._end = pt
        self._heightmap[pt] = ord('z') - baseline_height
      else:
        self._heightmap[pt] = ord(height_char) - baseline_height
    self._rows += 1

  def shortest_path_len(self) -> int:
    pq: List[Path] = []
    self._fewest_steps_to_reach[self._end] = 0
    for pt in self._reachable_points(self._end):
      heapq.heappush(pq, Path(
        self,
        1,
        pt,
        set([pt, self._end]),
      ))
    while True:
      path = heapq.heappop(pq)
      if self.height(path.point) == 0:
        return path.steps
      for pt in self._reachable_points(path.point):
        if (
          pt not in path.visited
        ) and ((
          pt not in self._fewest_steps_to_reach
        ) or (
          self._fewest_steps_to_reach[pt] > path.steps + 1
        )):
          steps = path.steps + 1
          self._fewest_steps_to_reach[pt] = steps
          heapq.heappush(
            pq,
            Path(
              self,
              steps,
              pt,
              set([pt, *path.visited]),
            ),
          )
    
def parse_input(filename: str) -> Heightmap:
  heightmap = Heightmap()
  with open(filename) as f:
    for l in f:
      heightmap.add_row(l.rstrip())
  return heightmap

if __name__ == '__main__':
  heightmap = parse_input('input.txt')
  print(heightmap.shortest_path_len())