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
    risk: int,
    point: Point,
    visited: Set[Point],
  ):
    self.risk = risk
    self.point = point
    self.visited = visited
    self.counter: int = next(counter)

  def __lt__(self, other: Path):
    if self.risk != other.risk:
      return self.risk < other.risk
    elif self.point.x + self.point.y != other.point.x + other.point.y:
      return self.point.x + self.point.y > other.point.x + other.point.y
    else:
      return self.counter < other.counter

  def __str__(self):
    return (
      '\n' +
      f"Point: {self.point}\n" +
      f"Risk: {self.risk}\n" +
      f"Visited: {self.visited}"
      '\n'
    )

class Riskmap:
  def __init__(self):
    self._riskmap: Dict[Point, int] = {}
    self._lowest_risk_to_reach: Dict[Point, int] = {
      Point(0, 0): 0,
    }
    self._cols = 0
    self._rows = 0

  def _rows(self) -> int:
    return self._rows_added * 5

  def adjacent_points(self, point: Point) -> Set[Point]:
    adj = set()
    if point.x != 0: adj.add(Point(point.x - 1, point.y))
    if point.y != 0: adj.add(Point(point.x, point.y - 1))
    if point.x != self._cols - 1: adj.add(Point(point.x + 1, point.y))
    if point.y != self._rows - 1: adj.add(Point(point.x, point.y + 1))
    return adj
    
  def add_row(self, row: str):
    if self._cols > 0: assert len(row) == self._cols
    else: self._cols = len(row)
    for x, risk in enumerate(row):
      self._riskmap[Point(x, self._rows)] = int(risk)
    self._rows += 1

  def _expanded_risk(self, original_point: Point, times_expanded: int) -> int:
    return ((self._riskmap[original_point] - 1 + times_expanded) % 9) + 1

  def expand_tiles(self, times):
    for horizontal_expansion in range(times):
      for vertical_expansion in range(times):
        if horizontal_expansion == 0 and vertical_expansion == 0:
          continue
        else:
          for x in range(self._cols):
            for y in range(self._rows):
              self._riskmap[Point(
                x + horizontal_expansion * self._cols,
                y + vertical_expansion * self._rows
              )] = self._expanded_risk(
                Point(x, y),
                horizontal_expansion + vertical_expansion
              )
    if times > 0:
      self._rows *= times
      self._cols *= times
          

  def lowest_risk(self, end_point: Point = None) -> int:
    if not end_point: end_point = Point(self._cols - 1, self._rows - 1)
    start_point = Point(0, 0)
    pq: List[Path] = []
    for pt in self.adjacent_points(start_point):
      heapq.heappush(pq, Path(
        self._riskmap[pt],
        pt,
        set([pt, start_point])
      ))
    while True:
      path = heapq.heappop(pq)
      if path.point not in self._lowest_risk_to_reach or self._lowest_risk_to_reach[path.point] > path.risk:
        self._lowest_risk_to_reach[path.point] = path.risk
      if path.point == end_point:
        return path.risk
      for pt in self.adjacent_points(path.point):
        if (
          pt not in path.visited
        ) and ((
          pt not in self._lowest_risk_to_reach
        ) or (
          self._lowest_risk_to_reach[pt] > path.risk + self._riskmap[pt]
        )):
          risk = path.risk + self._riskmap[pt]
          self._lowest_risk_to_reach[pt] = risk
          heapq.heappush(
            pq,
            Path(
              risk,
              pt,
              set([pt, *path.visited]),
            ),
          )
    
def parse_input(filename: str, times_expanded: int = 5) -> Riskmap:
  riskmap = Riskmap()
  with open(filename) as f:
    for l in f:
      riskmap.add_row(l.rstrip())
  riskmap.expand_tiles(times = times_expanded)
  return riskmap

if __name__ == '__main__':
  riskmap = parse_input('input.txt')
  print(riskmap.lowest_risk())