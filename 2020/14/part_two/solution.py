import re
import itertools
from typing import Union, Dict

from shared import SolutionABC

MASK_RE = re.compile(r"mask = (?P<mask>[01X]{36})")
MEM_RE = re.compile(r"mem\[(?P<addr>\d+)\] = (?P<val>\d+)")

class Solution(SolutionABC):
  def __init__(
    self,
  ):
    self._mask: str = None
    self._mem: Dict[int, int] = {}

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
      self._mem[addr] = val

  def parse_row(
    self,
    row: str,
  ):
    m = MASK_RE.match(row)
    if m is not None:
      self._mask = m['mask']
    else:
      m = MEM_RE.match(row)
      assert m
      addr = int(m['addr'])
      floating_addr = self._apply_mask(addr)
      val = int(m['val'])
      self._write_vals(floating_addr, val)

  def solve(
    self,
  ) -> Union[int, str]:
    return sum(val for val in self._mem.values())