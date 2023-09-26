from typing import List, Set

from solutions.shared import SolutionABC

class Solution(SolutionABC):
  def __init__(
    self,
  ):
    self.nums: List[int] = []

  def parse_row(
    self,
    row: str,
  ):
    self.nums.append(int(row))

  def first_repeated_frequency(
    self,
  ) -> int:
    frequencies: Set[int] = set([0])
    freq = 0
    i = 0
    while True:
      freq += self.nums[i]
      if freq in frequencies:
        return freq
      frequencies.add(freq)
      i = (i + 1) % len(self.nums)
    

  def solve(
    self,
  ) -> int:
    return self.first_repeated_frequency()