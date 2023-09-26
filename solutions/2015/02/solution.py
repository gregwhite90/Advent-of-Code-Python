import math
from typing import List

from solutions.shared import SolutionABC

class Box:
  def __init__(self, row: str):
    self.dimensions: List[int] = [int(dim) for dim in row.split('x')]
    self.sides: List[int] = [
      self.dimensions[0] * self.dimensions[1],
      self.dimensions[0] * self.dimensions[2],
      self.dimensions[1] * self.dimensions[2],
    ]
    self.perimeters: List[int] = [
      2 * sum(self.dimensions[:2]),
      2 * (self.dimensions[0] + self.dimensions[2]),
      2 * sum(self.dimensions[1:]),
    ]

  def surface_area(self) -> int:
    return 2 * sum(self.sides)

  def slack(self) -> int:
    return min(self.sides)

  def volume(self) -> int:
    return math.prod(self.dimensions)

  def min_perimeter(self) -> int:
    return min(self.perimeters)

class Solution(SolutionABC):
  def __init__(
    self,
  ):
    self.boxes: List[Box] = []

  def parse_row(
    self,
    row: str,
  ):
    self.boxes.append(Box(row))

  def solve(
    self,
  ) -> int:
    return sum(b.volume() + b.min_perimeter() for b in self.boxes)