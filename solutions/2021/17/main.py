import re
import itertools
from collections import defaultdict
from typing import NamedTuple

ROW_RE = re.compile(r"target area: x=(?P<left>\d+)\.\.(?P<right>\d+), y=(?P<bottom>\-\d+)\.\.(?P<top>\-\d+)")

class Target(NamedTuple):
  left: int
  right: int
  bottom: int
  top: int

class Velocity(NamedTuple):
  x: int
  y: int

class Probe:
  def __init__(self, row: str):
    m = ROW_RE.match(row)
    assert m
    self._target = Target(
      int(m['left']),
      int(m['right']),
      int(m['bottom']),
      int(m['top']),
    )
    assert self._target.left >= 0 and self._target.right >= 0 and self._target.right >= self._target.left
    assert self._target.bottom < 0 and self._target.top < 0 and self._target.bottom <= self._target.top
    self._steps_in_tgt = defaultdict(lambda: defaultdict(list))
    self._solve_y()
    self._solve_x()

  def _solve_y(self):
    min_init_y = self._target.bottom
    max_init_y = - self._target.bottom - 1
    for init_y in range(min_init_y, max_init_y + 1):
      step = 0
      y = 0
      vel = init_y
      while True:
        if y < self._target.bottom: break
        step += 1
        y += vel
        vel -= 1
        if y <= self._target.top and y >= self._target.bottom:
          self._steps_in_tgt[step]['y'].append(init_y)

  def _solve_x(self):
    min_init_x = 0
    max_init_x = self._target.right
    for init_x in range(min_init_x, max_init_x + 1):
      step = 0
      x = 0
      vel = init_x
      while True:
        if x > self._target.right: break
        elif vel == 0:
          if self._x_in_target(x):
            for steps, init_vels in self._steps_in_tgt.items():
              if steps >= step:
                init_vels['x'].append(init_x)
          break
        else:
          step += 1
          x += vel
          vel -= 1
          if self._x_in_target(x):
            self._steps_in_tgt[step]['x'].append(init_x)

  def _x_in_target(self, x: int) -> bool:
    return x >= self._target.left and x <= self._target.right

  def num_init_vels_in_tgt(self) -> int:
    init_vels_in_tgt = set()
    for init_vels in self._steps_in_tgt.values():
      for x, y in itertools.product(
        init_vels['x'],
        init_vels['y'],
      ):
        init_vels_in_tgt.add(
          Velocity(x, y)
        )
    return len(init_vels_in_tgt)

def parse_input(filename: str) -> Probe:
  probes = []
  with open(filename) as f:
    for l in f:
      probes.append(Probe(l.rstrip()))
  assert len(probes) == 1
  return probes[0]

if __name__ == '__main__':
  probe = parse_input('input/input.txt')
  print(probe.num_init_vels_in_tgt())