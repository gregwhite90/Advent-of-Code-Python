import re
from typing import Union, List

from shared import SolutionABC

REPEAT_SUBSTR_RE = re.compile(r'(\w\w)\w*\1')
REPEAT_RE = re.compile(r'(\w)\w\1')

class SantaString:
  def __init__(self, row: str):
    self.data = row
    self.nice = self._calculate_if_nice()

  def _calculate_if_nice(self) -> bool:
    return REPEAT_SUBSTR_RE.search(self.data) is not None and REPEAT_RE.search(self.data) is not None

  def is_nice(self) -> bool:
    return self.nice

class Solution(SolutionABC):
  def __init__(
    self,
  ):
    self.santa_strs: List[SantaString] = []

  def parse_row(
    self,
    row: str,
  ):
    self.santa_strs.append(SantaString(row))

  def solve(
    self,
  ) -> Union[int, str]:
    return sum(s.is_nice() for s in self.santa_strs)