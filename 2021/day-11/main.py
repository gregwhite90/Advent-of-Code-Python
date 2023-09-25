import itertools
from collections import namedtuple
from typing import Set

Point = namedtuple(
  'Point',
  ['x', 'y'],
)

class Grid:
  def __init__(self):
    self._values = {}
    self._rows = 0
    self._cols = 0
    self._flashes = []

  def add_row(self, row: str):
    if self._cols > 0:
      assert len(row) == self._cols
    else:
      self._cols = len(row)

    for col, value_str in enumerate(row):
      self._values[Point(col, self._rows)] = int(value_str)
    
    self._rows += 1
    
  def _adjacent_points(self, point: Point) -> Set[Point]:
    return set(filter(
      lambda pt: pt != point and pt.x >= 0 and pt.x < self._cols and pt.y >= 0 and pt.y < self._rows,
      set(
        Point(*pt)
        for pt
        in itertools.product(
          [point.x - 1, point.x, point.x + 1],
          [point.y - 1, point.y, point.y + 1],
        )
      )
    ))

  def _one_step(self):
    points_flashed = set()
    points_to_flash = set()
    for point in self._values.keys():
      self._values[point] += 1
      if self._values[point] > 9:
        points_to_flash.add(point)
    while len(points_to_flash) > 0:
      point = points_to_flash.pop()
      for adj in self._adjacent_points(point):
        self._values[adj] += 1
        if self._values[adj] > 9 and adj not in points_flashed:
          points_to_flash.add(adj)
      points_flashed.add(point)

    for point in points_flashed:
      self._values[point] = 0
    self._flashes.append(len(points_flashed))

  def n_steps(self, n: int):
    for _ in range(n):
      self._one_step()

  def total_flashes(self) -> int:
    return sum(self._flashes)

  def first_synced_flash(self) -> int:
    try:
      return self._flashes.index(self._rows * self._cols) + 1
    except ValueError:
      while True:
        self._one_step()
        if self._flashes[-1] == self._rows * self._cols:
          return len(self._flashes)

def parse_input(filename: str) -> Grid:
  grid = Grid()
  with open(filename) as f:
    for l in f:
      grid.add_row(l.rstrip())
  return grid

if __name__ == '__main__':
  grid = parse_input('input.txt')
  grid.n_steps(100)
  print(grid.total_flashes())
  print(grid.first_synced_flash())