import hashlib
from typing import Union

from shared import SolutionABC

class Solution(SolutionABC):
  def __init__(
    self,
  ):
    self.key: str = None

  def parse_row(
    self,
    row: str,
  ):
    self.key = row

  def solve(
    self,
  ) -> Union[int, str]:
    i = 1
    while True:
      hash = hashlib.md5(f"{self.key}{i}".encode()).hexdigest()
      if hash[:6] == '000000':
        break
      i += 1
    return i