from __future__ import annotations
from typing import NamedTuple, Set, List

from solutions.shared import SolutionABC

class Point(NamedTuple):
  x: int
  y: int
  z: int

class BoundingBox(NamedTuple):
  min_x: int
  min_y: int
  min_z: int
  max_x: int
  max_y: int
  max_z: int

def adjacent_points(point: Point) -> Set[Point]:
  return {
    Point(point.x - 1, point.y, point.z),
    Point(point.x + 1, point.y, point.z),
    Point(point.x, point.y - 1, point.z),
    Point(point.x, point.y + 1, point.z),
    Point(point.x, point.y, point.z - 1),
    Point(point.x, point.y, point.z + 1),
  }

class ConnectedPoints:
  def __init__(self):
    self.points: Set[Point] = set()
    self.bounding_box: BoundingBox = None

  def point_is_adjacent(self, point: Point) -> bool:
    for adj in adjacent_points(point):
      if adj in self.points:
        return True
    return False

  def add_point(self, point: Point):
    self._update_bounding_box(point)
    self.points.add(point)

  def total_sides(self) -> int:
    return sum(
      adj not in self.points
      for point in self.points
      for adj in adjacent_points(point)
    )

  def absorb(self, other: ConnectedPoints):
    self.points |= other.points
    self.bounding_box = BoundingBox(
      min(self.bounding_box.min_x, other.bounding_box.min_x),
      min(self.bounding_box.min_y, other.bounding_box.min_y),
      min(self.bounding_box.min_z, other.bounding_box.min_z),
      max(self.bounding_box.max_x, other.bounding_box.max_x),
      max(self.bounding_box.max_y, other.bounding_box.max_y),
      max(self.bounding_box.max_z, other.bounding_box.max_z),
    )

  def _update_bounding_box(self, point: Point):
    if self.bounding_box is None:
      self.bounding_box = BoundingBox(
        *point, *point
      )
    else:
      self.bounding_box = BoundingBox(
        min(point.x, self.bounding_box.min_x),
        min(point.y, self.bounding_box.min_y),
        min(point.z, self.bounding_box.min_z),
        max(point.x, self.bounding_box.max_x),
        max(point.y, self.bounding_box.max_y),
        max(point.z, self.bounding_box.max_z),
      )

class AirPockets:
  def __init__(self):
    self.pockets: List[ConnectedPoints] = []

  def add_point(self, point: Point):
    for pocket in self.pockets:
      if point in pocket.points:
        return
    adj_pocket_idxs = [i for i, pocket in enumerate(self.pockets) if pocket.point_is_adjacent(point)]
    if len(adj_pocket_idxs) == 0:
      new_pocket = ConnectedPoints()
      new_pocket.add_point(point)
      self.pockets.append(new_pocket)
    else:
      self.pockets[adj_pocket_idxs[0]].add_point(point)
      if len(adj_pocket_idxs) > 1:
        for idx in adj_pocket_idxs[1:]:
          self.pockets[adj_pocket_idxs[0]].absorb(self.pockets[idx])
        for order, idx in enumerate(adj_pocket_idxs[1:]):
          # repeat the for loop to avoid changing indices while still potentially absorbing
          self.pockets.pop(idx- order)

  def expand_air_pockets(self, rock: ConnectedPoints):
    points_to_add = self._expanding_air_pocket_points(rock)
    while len(points_to_add) > 0:
      for point in points_to_add:
        self.add_point(point)
      points_to_add = self._expanding_air_pocket_points(rock)

  def _expanding_air_pocket_points(self, rock: ConnectedPoints) -> Set[Point]:
    points_to_add = set()
    for pocket in self.pockets:
      for point in pocket.points:
        for adj in adjacent_points(point):
          if adj not in rock.points and adj not in pocket.points and (
            adj.x >= rock.bounding_box.min_x - 1 and
            adj.x <= rock.bounding_box.max_x + 1 and
            adj.y >= rock.bounding_box.min_y - 1 and
            adj.y <= rock.bounding_box.max_y + 1 and
            adj.z >= rock.bounding_box.min_z - 1 and
            adj.z <= rock.bounding_box.max_z + 1
          ):
            points_to_add.add(adj)
    return points_to_add

  def internal_sides(self, rock: ConnectedPoints) -> int:
    internal_sides = 0
    for pocket in self.pockets:
      if (
        pocket.bounding_box.min_x < rock.bounding_box.min_x or
        pocket.bounding_box.min_y < rock.bounding_box.min_y or
        pocket.bounding_box.min_z < rock.bounding_box.min_z or
        pocket.bounding_box.max_x > rock.bounding_box.max_x or
        pocket.bounding_box.max_y > rock.bounding_box.max_y or
        pocket.bounding_box.max_z > rock.bounding_box.max_z
      ):
        continue
      internal_sides += pocket.total_sides()
    return internal_sides

class Solution(SolutionABC):
  def __init__(
    self,
  ):
    self.rock = ConnectedPoints()
    self.air_pockets = AirPockets()

  def parse_row(
    self,
    row: str,
  ):
    self.rock.add_point(Point(
      *[int(coord) for coord in row.split(',')]
    ))

  def solve(
    self,
  ) -> int:
    self._create_air_pockets()
    self._expand_air_pockets()
    return self.rock.total_sides() - self.air_pockets.internal_sides(self.rock)

  def _create_air_pockets(self):
    for pt in self.rock.points:
      for adj in adjacent_points(pt):
        if adj not in self.rock.points:
          self.air_pockets.add_point(adj)

  def _expand_air_pockets(self):
    self.air_pockets.expand_air_pockets(self.rock)