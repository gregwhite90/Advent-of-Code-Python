from typing import Union

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
    for noun in range(100):
      for verb in range(100):
        intcode_computer = IntcodeComputer([self.base_program[0]] + [noun] + [verb] + self.base_program[3:])
        intcode_computer.run()
        if intcode_computer.position_0() == 19690720:
          return 100 * noun + verb
