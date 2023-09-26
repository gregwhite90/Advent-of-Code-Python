from typing import List, NamedTuple, Dict

from solutions.shared import SolutionABC, IntcodeComputer, InputMode

class Position(NamedTuple):
  x: int
  y: int

class Boundary(NamedTuple):
  min: int
  max: int

BEAM_TO_STR = {
  0: ' ',
  1: '#',
}

DIMS = 45

class Solution(SolutionABC):
  def __init__(
    self,
  ):
    self.base_program: List[int] = None
    self.boundaries: Dict[int, Boundary] = {}

  def parse_row(
    self,
    row: str,
  ):
    self.base_program = [int(val) for val in row.split(',')]

  def __str__(self) -> str:
    res = ''
    for y in range(DIMS):
      for x in range(DIMS):
        res += BEAM_TO_STR[self.beam[Position(x, y)]]
      res += '\n'
    return res

  def get_output(self, x: int, y: int) -> int:
    ic = IntcodeComputer(
      self.base_program.copy(),
      [x, y],
      [InputMode.CONNECTED, InputMode.CONNECTED],
    )
    ic.run()
    return ic.get_outputs()[0]

  def solve(
    self,
  ) -> int:
    y = 0
    x = 0
    while True:
      output = self.get_output(x, y)
      while output == 0:
        x += 1
        output = self.get_output(x, y)
      min_x = x
      if y >= 100 and self.boundaries[y - 100 + 1].max >= min_x + 100 - 1:
        return 10000 * min_x + (y - 100 + 1)
      x += 0 if y == 0 else self.boundaries[y - 1].max - self.boundaries[y - 1].min
      while output == 1:
        x += 1
        output = self.get_output(x, y)
      max_x = x - 1
      self.boundaries[y] = Boundary(min_x, max_x)
      y += 1
      x = min_x