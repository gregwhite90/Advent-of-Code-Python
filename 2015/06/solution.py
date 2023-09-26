import re
from typing import Union, List

from shared import SolutionABC

COLS = 1000
ROWS = 1000

ROW_RE = re.compile(r'(?P<operation>toggle|turn on|turn off) (?P<x_0>\d+),(?P<y_0>\d+) through (?P<x_1>\d+),(?P<y_1>\d+)')

class Solution(SolutionABC):
  def __init__(
    self,
  ):
    self.lights: List[List[bool]] = [[False] * COLS] * ROWS

  def parse_row(
    self,
    row: str,
  ):
    m = ROW_RE.match(row)
    assert m is not None
    for x in range(int(m['x_0']), int(m['x_1']) + 1):
      for y in range(int(m['y_0']), int(m['y_1']) + 1):
        if m['operation'] == 'turn on':
          self.lights[x][y] = True
        elif m['operation'] == 'turn off':
          self.lights[x][y] == False
        else:
          assert m['operation'] == 'toggle'
          self.lights[x][y] = not self.lights[x][y]
        
  def solve(
    self,
  ) -> Union[int, str]:
    return sum(sum(l for l in row) for row in self.lights)