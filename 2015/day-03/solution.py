from typing import Union, NamedTuple, Set, List

from shared import SolutionABC

class Point(NamedTuple):
  x: int
  y: int

class Solution(SolutionABC):
  def __init__(
    self,
  ):
    self.locns: List[Point] = [Point(0, 0), Point(0, 0)]
    self.visited: Set[Point] = {self.locns[0]}

  def parse_row(
    self,
    row: str,
  ):
    for i, char in enumerate(row):
      if char == '^':
        self.locns[i % 2] = Point(self.locns[i % 2].x, self.locns[i % 2].y + 1)
      elif char == 'v':
        self.locns[i % 2] = Point(self.locns[i % 2].x, self.locns[i % 2].y - 1)
      elif char == '<':
        self.locns[i % 2] = Point(self.locns[i % 2].x - 1, self.locns[i % 2].y)
      else:
        assert char == '>'
        self.locns[i % 2] = Point(self.locns[i % 2].x + 1, self.locns[i % 2].y)
      self.visited.add(self.locns[i % 2])

  def solve(
    self,
  ) -> Union[int, str]:
    return len(self.visited)