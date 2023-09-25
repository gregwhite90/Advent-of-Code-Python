from typing import Union, NamedTuple, Dict
from enum import Enum

from shared import SolutionABC

class PixelStatus(Enum):
  LIGHT = '#'
  DARK = '.'

PIXEL_VALUE = {
  PixelStatus.LIGHT: '1',
  PixelStatus.DARK: '0',
}

class Point(NamedTuple):
  x: int
  y: int

class BoundingBox(NamedTuple):
  min_x: int
  min_y: int
  max_x: int
  max_y: int

class Image:
  def __init__(self, outside_boundary: PixelStatus):
    # TODO: figure out initialization if any.
    self.pixels: Dict[Point, PixelStatus] = {}
    self.bounding_box: BoundingBox = BoundingBox(
      0,
      0,
      0,
      0,
    )
    self.outside_boundary = outside_boundary

  def add_row(self, row: str):
    for x, char in enumerate(row):
      self.pixels[Point(x, self.bounding_box.max_y)] = PixelStatus(char)
    self.bounding_box = BoundingBox(
      0,
      0,
      max(len(row), self.bounding_box.max_x),
      self.bounding_box.max_y + 1,
    )

  def update_starting_bounding_box(self):
    self.bounding_box = BoundingBox(
      0,
      0,
      self.bounding_box.max_x - 1,
      self.bounding_box.max_y - 1,
    )

  def _enhance_pixel(self, point: Point, algorithm: str) -> PixelStatus:
    binary_str = ''
    for y in range(point.y - 1, point.y + 2):
      for x in range(point.x - 1, point.x + 2):
        pt = Point(x, y)
        if pt in self.pixels:
          binary_str += PIXEL_VALUE[self.pixels[pt]]
        else:
          binary_str += PIXEL_VALUE[self.outside_boundary]
    index = int(binary_str, 2)
    return PixelStatus(algorithm[index])
  
  def enhance(self, algorithm: str):
    self.bounding_box = BoundingBox(
      self.bounding_box.min_x - 2,
      self.bounding_box.min_y - 2,
      self.bounding_box.max_x + 2,
      self.bounding_box.max_y + 2,
    )
    new_pixels: Dict[Point, PixelStatus] = {}
    for x in range(self.bounding_box.min_x, self.bounding_box.max_x + 1):
      for y in range(self.bounding_box.min_y, self.bounding_box.max_y + 1):
        pt = Point(x, y)
        new_pixels[pt] = self._enhance_pixel(pt, algorithm)
    self.pixels = new_pixels
    ob_index = int(PIXEL_VALUE[self.outside_boundary] * 9, 2)
    self.outside_boundary = PixelStatus(algorithm[ob_index])

  def num_light_pixels(self) -> int:
    assert self.outside_boundary == PixelStatus.DARK
    return len(set(p for p, status in self.pixels.items() if status == PixelStatus.LIGHT))

  def __str__(self) -> str:
    res = ''
    for y in range(self.bounding_box.min_y, self.bounding_box.max_y + 1):
      for x in range(self.bounding_box.min_x, self.bounding_box.max_x + 1):
        res += self.pixels[Point(x, y)].value
      res += '\n'
    return res

class Solution(SolutionABC):
  def __init__(
    self,
  ):
    self.algorithm: str = None
    self.image = Image(PixelStatus.DARK)
    self.parsing_image = False

  def parse_row(
    self,
    row: str,
  ):
    if len(row) == 0:
      self.parsing_image = True
    else:
      if not self.parsing_image:
        self.algorithm = row
      else:
        self.image.add_row(row)

  def solve(
    self,
  ) -> Union[int, str]:
    self.image.update_starting_bounding_box()
    for _ in range(50):
      self.image.enhance(self.algorithm)
    return self.image.num_light_pixels()