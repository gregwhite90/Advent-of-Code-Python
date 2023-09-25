from collections import defaultdict, namedtuple
from typing import Generator

Coordinates = namedtuple(
  "Coordinates",
  ["x", "y"],
)

class Line:
  def __init__(
    self,
    start_coords: Coordinates,
    end_coords: Coordinates,
  ):
    self._start_coords = start_coords
    self._end_coords = end_coords

  def is_point(self):
    return self._start_coords.y == self._end_coords.y and self._start_coords.x == self._end_coords.x

  def is_horizontal(self) -> bool:
    return not self.is_point() and self._start_coords.y == self._end_coords.y

  def is_vertical(self) -> bool:
    return not self.is_point() and self._start_coords.x == self._end_coords.x

  def is_diagonal(self) -> bool:
    return not self.is_point() and abs(self._start_coords.x - self._end_coords.x) == abs(self._start_coords.y - self._end_coords.y)

  def all_coordinates(self) -> Generator[Coordinates, None, None]:
    if self.is_point():
      yield Coordinates(self._start_coords.x, self._start_coords.y)
    elif self.is_horizontal():
      min_x, max_x = (
        (self._start_coords.x, self._end_coords.x)
        if self._end_coords.x >= self._start_coords.x
        else (self._end_coords.x, self._start_coords.x)
      )
      x = min_x
      while x <= max_x:
        yield Coordinates(x, self._start_coords.y)
        x += 1
    elif self.is_vertical():
      min_y, max_y = (
        (self._start_coords.y, self._end_coords.y)
        if self._end_coords.y >= self._start_coords.y
        else (self._end_coords.y, self._start_coords.y)
      )
      y = min_y
      while y <= max_y:
        yield Coordinates(self._start_coords.x, y)
        y += 1
    elif self.is_diagonal():
      x_step = (
        -1
        if self._start_coords.x > self._end_coords.x
        else 1
      )
      y_step = (
        -1
        if self._start_coords.y > self._end_coords.y
        else 1
      )
      coords = self._start_coords
      while coords != self._end_coords:
        yield coords
        coords = Coordinates(coords.x + x_step, coords.y + y_step)
      yield self._end_coords

class VentField:
  def __init__(self):
    self._vents = defaultdict(int)

  def add_line(self, line: Line):
    for coord in line.all_coordinates():
      self._vents[coord] += 1

  def points_with_more_vents(
    self,
    more_than_vents: int = 1,
  ):
    return sum(vents > more_than_vents for vents in self._vents.values())

def parse_input(filename: str) -> VentField:
  vent_field = VentField()
  with open(filename) as infile:
    for l in infile:
      line = Line(*[parse_coord(coord_str) for coord_str in l.split('->')])
      vent_field.add_line(line)     
  return vent_field

def parse_coord(coord_str: str) -> Coordinates:
  return Coordinates(*[int(coord_component) for coord_component in coord_str.split(',')])

if __name__ == '__main__':
  vent_field = parse_input('input.txt')
  print(vent_field.points_with_more_vents())