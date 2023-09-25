import re
from typing import List

NOOP_RE = re.compile(r"noop")
ADDX_RE = re.compile(r"addx (?P<value>\-?\d+)")
NOOP_CYCLES = 1
ADDX_CYCLES = 2

class CPU:
  def __init__(self):
    self._x_values: List[int] = [1]

  def parse_row(self, row: str):
    if NOOP_RE.match(row):
      for _ in range(NOOP_CYCLES):
        self._x_values.append(self._x_values[-1])
    else:
      m = ADDX_RE.match(row)
      assert m
      delta = int(m["value"])
      for _ in range(ADDX_CYCLES - 1):
        self._x_values.append(self._x_values[-1])
      self._x_values.append(self._x_values[-1] + delta)

  def _signal_during_cycle(self, cycle_num: int) -> int:
    return cycle_num * self._x_values[cycle_num - 1]

  def sum_signals(
    self,
    cycles: List[int] = [20, 60, 100, 140, 180, 220]
  ) -> int:
    return sum(
      self._signal_during_cycle(cycle_num)
      for cycle_num in cycles
    )

  def draw(
    self,
    cycles: int = 240,
    row_len: int = 40,
    sprite_len: int = 3,
  ) -> str:
    assert sprite_len > 0 and sprite_len % 2 == 1
    offset = (sprite_len - 1) // 2
    output = ''
    for cycle in range(1, cycles + 1):
      pos = (cycle - 1) % row_len
      val = self._x_values[cycle - 1]
      if pos >= val - offset and pos <= val + offset:
        output += '#'
      else:
        output += '.'
      if cycle % row_len == 0:
        output += '\n'
    return output

def parse_input(filename: str) -> CPU:
  cpu = CPU()
  with open(filename) as f:
    for l in f:
      cpu.parse_row(l.rstrip())
  return cpu

if __name__ == '__main__':
  cpu = parse_input('input.txt')
  print(cpu.sum_signals())
  print(cpu.draw())