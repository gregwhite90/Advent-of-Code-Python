from itertools import permutations
from typing import Union, List

from shared import SolutionABC, IntcodeComputer, InputMode

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
    max_thruster_signal = 0
    for perm in permutations(range(5, 10)):
      amplifiers = [IntcodeComputer(
        self.base_program.copy(), 
        [perm[0], 0],
        [InputMode.CONNECTED, InputMode.CONNECTED],
      )]
      amplifiers[-1].run()
      for i in range(4):      
        amplifiers.append(IntcodeComputer(
          self.base_program.copy(), 
          [perm[i + 1], amplifiers[-1].get_outputs()[-1]],
          [InputMode.CONNECTED, InputMode.CONNECTED],
        ))
        amplifiers[-1].run()
      i = 0
      while True:
        if amplifiers[i].is_halted(): break
        amplifiers[i].enqueue_input(amplifiers[i - 1].get_outputs()[-1])
        amplifiers[i].run()
        i = (i + 1) % len(amplifiers)
      max_thruster_signal = max(max_thruster_signal, amplifiers[-1].get_outputs()[-1])
    return max_thruster_signal