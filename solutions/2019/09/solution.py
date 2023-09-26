from typing import List

from solutions.shared import SolutionABC, IntcodeComputer, InputMode

class Solution(SolutionABC):
  def __init__(
    self,
  ):
    self.base_program: List[int] = None

  def parse_row(
    self,
    row: str,
  ):
    self.base_program = [int(val) for val in row.split(',')]

  def solve(
    self,
  ) -> int:
    ic = IntcodeComputer(self.base_program, [2], [InputMode.CONNECTED])
    ic.run()
    return ic.get_outputs()[0]