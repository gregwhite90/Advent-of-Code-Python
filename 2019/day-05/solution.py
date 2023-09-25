from typing import Union, List

from shared import SolutionABC, IntcodeComputer

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
  ) -> Union[int, str]:
    intcode_computer = IntcodeComputer(self.base_program)
    intcode_computer.run()