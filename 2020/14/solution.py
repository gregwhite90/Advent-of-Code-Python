import re
import itertools
from typing import Union, Dict, Tuple

from shared import SolutionABC

MASK_RE = re.compile(r"mask = (?P<mask>[01X]{36})")
MEM_RE = re.compile(r"mem\[(?P<addr>\d+)\] = (?P<val>\d+)")

class Solution(SolutionABC):
  def __init__(
    self,
  ):
    self._part_one_mem: Dict[int, int] = {}
    self._cur_and_mask = None
    self._cur_or_mask = None
    self._mask: str = None
    self._part_two_mem: Dict[int, int] = {}

  def _apply_mask(self, addr: int) -> str:
    assert self._mask is not None
    addr_str = f'{addr:036b}'
    res = ''
    for i, char in enumerate(self._mask):
      if char == '0':
        res += addr_str[i]
      else:
        res += char
    return res

  def _write_vals(self, floating_addr: str, val: int):
    for addr_bits in itertools.product(range(2), repeat=floating_addr.count('X')):
      addr_bits_iter = iter(addr_bits)
      addr_str = re.sub('X', lambda _ : str(next(addr_bits_iter)), floating_addr)
      addr = int(addr_str, 2)
      self._part_two_mem[addr] = val

  def parse_row(
    self,
    row: str,
  ):
    m = MASK_RE.match(row)
    if m is not None:
      # part one
      self._cur_and_mask = int(m['mask'].replace('X', '1'), 2)
      self._cur_or_mask = int(m['mask'].replace('X', '0'), 2)
      # part two
      self._mask = m['mask']
    else:
      m = MEM_RE.match(row)
      assert m
      # part one
      self._part_one_mem[m['addr']] = \
        int(m['val']) & \
        self._cur_and_mask | \
        self._cur_or_mask
      # part two
      addr = int(m['addr'])
      floating_addr = self._apply_mask(addr)
      val = int(m['val'])
      self._write_vals(floating_addr, val)

  def solve(
    self,
  ) -> Tuple[int]:
    return (
      sum(self._part_one_mem.values()),
      sum(self._part_two_mem.values()),
    )