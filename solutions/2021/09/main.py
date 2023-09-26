import math
from collections import namedtuple
from typing import Set

Coordinates = namedtuple(
  'Coordinates',
  ['x', 'y'],
)

class Heightmap:
  def __init__(self):
    self._heightmap = {}
    self._rows = 0
    self._cols = 0

  def add_row(self, row: str):
    if self._cols > 0:
      assert len(row) == self._cols
    else:
      self._cols = len(row)

    for col, height_str in enumerate(row):
      self._heightmap[Coordinates(col, self._rows)] = int(height_str)
    
    self._rows += 1
    
  def _adjacent_coords(self, coords: Coordinates) -> Set[Coordinates]:
    adjacent_coords = set()
    if coords.x != 0:
      adjacent_coords.add(Coordinates(coords.x - 1, coords.y))
    if coords.x != self._cols - 1:
      adjacent_coords.add(Coordinates(coords.x + 1, coords.y))
    if coords.y != 0:
      adjacent_coords.add(Coordinates(coords.x, coords.y - 1))
    if coords.y != self._rows - 1:
      adjacent_coords.add(Coordinates(coords.x, coords.y + 1))
    return adjacent_coords

  def _is_lowpoint(self, coords: Coordinates) -> bool:
    adjacent_coords = self._adjacent_coords(coords)
    for adj in adjacent_coords:
      if self._heightmap[adj] <= self._heightmap[coords]:
        return False
    return True

  def _all_lowpoints(self) -> Set[Coordinates]:
    return set(
      filter(
        lambda point: self._is_lowpoint(point),
        self._heightmap.keys()
      )
    )

  def risk_of_lowpoints(self) -> int:
    return sum(
      1 + self._heightmap[point]
      for point
      in self._all_lowpoints()
    )

  def _basin(self, point: Coordinates) -> Set[Coordinates]:
    basin = set([point])
    points_to_consider = set([point])
    while len(points_to_consider) > 0:
      cur = points_to_consider.pop()
      for adj in self._adjacent_coords(cur):
        if self._heightmap[adj] != 9 and adj not in basin and self._heightmap[adj] >= self._heightmap[cur]:
          basin.add(adj)
          points_to_consider.add(adj)
    return basin

  def top_n_basin_area_product(self, n: int = 3) -> int:
    basin_areas = [
      len(self._basin(lp))
      for lp
      in self._all_lowpoints()
    ]
    basin_areas.sort(reverse = True)
    return math.prod(basin_areas[:n])

def parse_input(filename: str) -> Heightmap:
  heightmap = Heightmap()
  with open(filename) as f:
    for l in f:
      heightmap.add_row(l.rstrip())
  return heightmap

if __name__ == '__main__':
  heightmap = parse_input('input/input.txt')
  print(heightmap.risk_of_lowpoints())
  print(heightmap.top_n_basin_area_product())