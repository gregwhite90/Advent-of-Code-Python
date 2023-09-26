from __future__ import annotations

import re
from typing import NamedTuple, List

from solutions.shared import SolutionABC

ROW_RE = re.compile(r"\<x\=(?P<x>\-?\d+), y\=(?P<y>\-?\d+), z=(?P<z>\-?\d+)\>")

class Vector(NamedTuple):
  x: int
  y: int
  z: int

  def __add__(self, other: Vector) -> Vector:
    return Vector(
      self.x + other.x,
      self.y + other.y,
      self.z + other.z,
    )

  def abs_sum(self) -> int:
    return abs(self.x) + abs(self.y) + abs(self.z)

class Moon:
  def __init__(
    self,
    pos: Vector,
  ):
    self.pos = pos
    self.vel = Vector(0, 0, 0)

  def update_velocity(
    self,
    update_vec: Vector,
  ):
    self.vel += update_vec

  def apply_velocity(
    self,
  ):
    self.pos += self.vel

  def potential_energy(self) -> int:
    return self.pos.abs_sum()

  def kinetic_energy(self) -> int:
    return self.vel.abs_sum()

  def total_energy(self) -> int:
    return self.potential_energy() * self.kinetic_energy()

  def __str__(
    self,
  ) -> str:
    return f'Position: {self.pos}\nVelocity: {self.vel}'

class Solution(SolutionABC):
  def __init__(
    self,
  ):
    self.moons: List[Moon] = []

  def parse_row(
    self,
    row: str,
  ):
    m = ROW_RE.match(row)
    assert m
    self.moons.append(
      Moon(
        Vector(int(m['x']), int(m['y']), int(m['z'])),
      )
    )

  def time_step(
    self,
  ):
    self.apply_gravity()
    self.apply_velocity()

  def apply_gravity(
    self,
  ):
    for i in range(len(self.moons) - 1):
      for j in range(i + 1, len(self.moons)):
        self.apply_pairwise_gravity(i, j)

  def apply_pairwise_gravity(
    self,
    i: int,
    j: int,
  ):
    i_to_j = Vector(
      *[
        (self.moons[j].pos[coord_idx] - self.moons[i].pos[coord_idx]) // abs(self.moons[j].pos[coord_idx] - self.moons[i].pos[coord_idx]) if self.moons[j].pos[coord_idx] != self.moons[i].pos[coord_idx] else 0
        for coord_idx in range(len(self.moons[i].pos))
      ]
    )
    j_to_i = Vector(
      *[
        -val for val in i_to_j
      ]
    )
    self.moons[i].update_velocity(i_to_j)
    self.moons[j].update_velocity(j_to_i)

  def update_velocity(
    self,
    idx: int,
    update_vec: Vector,
  ):
    self.moons[idx] = Moon(self.moons[idx].pos, Vector(
      self.moons[idx].vel.x + update_vec.x,
      self.moons[idx].vel.y + update_vec.y,
      self.moons[idx].vel.z + update_vec.z,
    ))

  def apply_velocity(
    self,
  ):
    for moon in self.moons:
      moon.apply_velocity()

  def solve(
    self,
  ) -> int:
    for _ in range(1000):
      self.time_step()
    return sum(moon.total_energy() for moon in self.moons)