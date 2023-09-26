"""
I used this comment to help figure out the overlapping off regions for part 2.
https://www.reddit.com/r/adventofcode/comments/rlxhmg/comment/hpizza8
"""
import re
import collections
from typing import NamedTuple, Counter

from solutions.shared import SolutionABC

STEP_RE = re.compile(r'(?P<operation>on|off) x=(?P<min_x>\-?\d+)\.\.(?P<max_x>\-?\d+),y=(?P<min_y>\-?\d+)\.\.(?P<max_y>\-?\d+),z=(?P<min_z>\-?\d+)\.\.(?P<max_z>\-?\d+)')

class Cuboid(NamedTuple):
  min_x: int
  min_y: int
  min_z: int
  max_x: int
  max_y: int
  max_z: int

def has_overlap(cuboid_0: Cuboid, cuboid_1: Cuboid) -> bool:
  return (
    cuboid_0.min_x <= cuboid_1.max_x and cuboid_0.max_x >= cuboid_1.min_x
  ) and (
    cuboid_0.min_y <= cuboid_1.max_y and cuboid_0.max_y >= cuboid_1.min_y
  ) and (
    cuboid_0.min_z <= cuboid_1.max_z and cuboid_0.max_z >= cuboid_1.min_z
  )

def overlapping_cuboid(cuboid_0: Cuboid, cuboid_1: Cuboid) -> Cuboid:
  assert has_overlap(cuboid_0, cuboid_1)
  return Cuboid(
    max(cuboid_0.min_x, cuboid_1.min_x),
    max(cuboid_0.min_y, cuboid_1.min_y),
    max(cuboid_0.min_z, cuboid_1.min_z),
    min(cuboid_0.max_x, cuboid_1.max_x),
    min(cuboid_0.max_y, cuboid_1.max_y),
    min(cuboid_0.max_z, cuboid_1.max_z),
  )

def volume(cuboid: Cuboid) -> int:
  return (
    cuboid.max_x - cuboid.min_x + 1
  ) * (
    cuboid.max_y - cuboid.min_y + 1
  ) * (
    cuboid.max_z - cuboid.min_z + 1
  )

class Solution(SolutionABC):
  def __init__(
    self,
  ):
    self.cuboids: Counter[Cuboid] = collections.Counter()

  def parse_row(
    self,
    row: str,
  ):
    m = STEP_RE.match(row)
    assert m
    cuboid = Cuboid(
      int(m['min_x']),
      int(m['min_y']),
      int(m['min_z']),
      int(m['max_x']),
      int(m['max_y']),
      int(m['max_z']),
    )
    update: Counter[Cuboid] = collections.Counter()
    for existing_cuboid, existing_sign in self.cuboids.items():
      if has_overlap(cuboid, existing_cuboid):
        update[overlapping_cuboid(cuboid, existing_cuboid)] -= existing_sign
    if m['operation'] == 'on':
      update[cuboid] += 1
    self.cuboids.update(update)

  def solve(
    self,
  ) -> int:
    return sum(volume(cuboid) * sign for cuboid, sign in self.cuboids.items())