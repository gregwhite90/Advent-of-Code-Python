import re
from typing import Dict, Union

from shared import SolutionABC

MASK_RE = re.compile(r"^mask = (?P<mask_bits>[01X]+)$")
MEM_RE = re.compile(r"^mem\[(?P<addr>\d+)\] = (?P<val>\d+)$")

class Solution(SolutionABC):
  def __init__(
    self,
  ):
    self._mask: str = None
    self._part_one_mem: Dict[int, int] = {}
    self._cur_and_mask = None
    self._cur_or_mask = None

  def parse_row(
    self,
    row: str,
  ):
    mask_match = MASK_RE.match(row)
    if mask_match is not None:
      self._cur_and_mask = int(mask_match['mask_bits'].replace('X', '1'), 2)
      self._cur_or_mask = int(mask_match['mask_bits'].replace('X', '0'), 2)
    mem_match = MEM_RE.match(row)
    if mem_match is not None:
      self._part_one_mem[mem_match['addr']] = \
        int(mem_match['val']) & \
        self._cur_and_mask | \
        self._cur_or_mask

  def solve(
    self,
  ) -> Union[int, str]:
    return sum(self._part_one_mem.values())