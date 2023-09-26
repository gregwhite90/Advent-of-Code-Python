import numpy as np
import numpy.typing

from solutions.shared import SolutionABC

BASE_PATTERN = np.array([0, 1, 0, -1])
INPUT_EXPANSION = 10000

def ones_digit(num: int) -> int:
  return abs(num) % 10

class Solution(SolutionABC):
  def __init__(
    self,
  ):
    self.relevant_signal: numpy.typing.ArrayLike = None
    self.offset: int = None

  def parse_row(
    self,
    row: str,
  ):
    self.offset = int(row[:7])
    signal = np.tile(np.array([int(char) for char in list(row)]), INPUT_EXPANSION)
    self.relevant_signal = signal[self.offset : ]
  
  def one_phase(
    self,
  ):
    res = np.empty(len(self.relevant_signal))
    res[-1] = self.relevant_signal[-1]
    for i in range(len(self.relevant_signal) - 2, -1, -1):
      res[i] = res[i + 1] + self.relevant_signal[i]
    self.relevant_signal = ones_digit(res)
      
  def solve(
    self,
  ) -> str:
    for _ in range(100):
      self.one_phase()
    return ''.join([str(int(signal)) for signal in self.relevant_signal[:8]])