import re
import itertools
from typing import NamedTuple, Set

ROW_RE = re.compile(r"(?P<direction>[RLUD]) (?P<steps>\d+)")

class Point(NamedTuple):
  x: int
  y: int

class RopeGrid:
  def __init__(
    self,
    start_point: Point = Point(0, 0),
    num_knots: int = 10
  ):
    self.knots = [start_point for _ in range(num_knots)]
    self.tail_visited = set([start_point])

  def _touching_points(self, point: Point) -> Set[Point]:
    return set(Point(x, y) for x, y in itertools.product(
      [point.x - 1, point.x, point.x + 1],
      [point.y - 1, point.y, point.y + 1],
    ))

  def _move_knot(self, index: int):
    assert index > 0 and index < len(self.knots)
    assert self.knots[index] not in self._touching_points(self.knots[index - 1])
    deltas = [
      0 if getattr(self.knots[index - 1], axis) == getattr(self.knots[index], axis)
      else (
        getattr(self.knots[index - 1], axis) - getattr(self.knots[index], axis)
      ) // (
        abs(getattr(self.knots[index - 1], axis) - getattr(self.knots[index], axis))
      )
      for axis in ['x', 'y']
    ]
    self.knots[index] = Point(
      self.knots[index].x + deltas[0], self.knots[index].y + deltas[1]
    )
    if index == len(self.knots) - 1:
      self.tail_visited.add(self.knots[index])

  def _move_head(self, dir: str, steps: int = 1):
    if dir == 'R':
      self.knots[0] = Point(
        self.knots[0].x + steps,
        self.knots[0].y
      )
    elif dir == 'L':
      self.knots[0] = Point(
        self.knots[0].x - steps,
        self.knots[0].y
      )
    elif dir == 'U':
      self.knots[0] = Point(
        self.knots[0].x,
        self.knots[0].y + steps
      )
    else:
      assert dir == 'D'
      self.knots[0] = Point(
        self.knots[0].x,
        self.knots[0].y - steps
      )

  def parse_row(self, row: str):
    m = ROW_RE.match(row)
    assert m
    steps = int(m['steps'])
    for _ in range(steps):
      self._move_head(m['direction'])
      for index in range(1, len(self.knots)):
        if self.knots[index] not in self._touching_points(self.knots[index - 1]):
          self._move_knot(index)

  def num_tail_visited(self):
    return len(self.tail_visited)

def parse_input(filename: str, num_knots: int = 10) -> RopeGrid:
  grid = RopeGrid(num_knots = num_knots)
  with open(filename) as f:
    for l in f:
      grid.parse_row(l.rstrip())
  return grid

if __name__ == '__main__':
  grid = parse_input('input.txt')
  print(grid.num_tail_visited())