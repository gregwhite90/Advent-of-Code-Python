import re
from typing import Union, NamedTuple, List

from shared import SolutionABC

ROW_RE = re.compile(r"Sensor at x=(?P<sensor_x>\-?\d+), y=(?P<sensor_y>\-?\d+): closest beacon is at x=(?P<beacon_x>\-?\d+), y=(?P<beacon_y>\-?\d+)")

class Point(NamedTuple):
  x: int
  y: int

def manhattan_distance(p_0: Point, p_1: Point) -> int:
  return abs(p_0.x - p_1.x) + abs(p_0.y - p_1.y)

class Range(NamedTuple):
  lo: int
  hi: int

def tuning_frequency(point: Point) -> int:
  return 4000000 * point.x + point.y

class Sensor:
  def __init__(self, pos: Point, beacon: Point):
    self.pos = pos
    self.beacon = beacon
    self.radius = manhattan_distance(pos, beacon)

  def blocked(self, y: int) -> Range:
    line_min_dist = abs(self.pos.y - y)
    margin = max(0, self.radius - line_min_dist)
    if margin > 0:
      return Range(
        self.pos.x - margin,
        self.pos.x + margin,
      )
    else:
      return None

  def is_blocked(self, point: Point) -> bool:
    r = self.blocked(point.y)
    return r and r.lo <= point.x and r.hi >= point.x

class Solution(SolutionABC):
  def __init__(
    self,
  ):
    self.sensors: List[Sensor] = []

  def parse_row(
    self,
    row: str,
  ):
    m = ROW_RE.match(row)
    assert m
    self.sensors.append(Sensor(
      Point(int(m['sensor_x']), int(m['sensor_y'])),
      Point(int(m['beacon_x']), int(m['beacon_y'])),
    ))

  def solve(
    self,
  ) -> Union[int, str]:
    self.sensors.sort(key=lambda s: s.pos.x)
    return tuning_frequency(self._empty_point())

  def _is_blocked(self, point: Point) -> bool:
    for sensor in self.sensors:
      if sensor.is_blocked(point):
        return True
    return False    

  def _empty_point(self) -> Point:
    """Finds the one empty point in the search area.

    Uses the insight that an empty point that's not on the border of the search area
    will be just out of range of multiple sensors (otherwise other points between
    those two sensors could be empty as well). Searches for points by finding
    pairs of sensors that share a 1-wide border just outside their range, and
    checking each of those points for whether they are out of range of all sensors.
    """
    for i in range(len(self.sensors)):
      for j in range(i + 1, len(self.sensors)):
        if manhattan_distance(self.sensors[i].pos, self.sensors[j].pos) == self.sensors[i].radius + self.sensors[j].radius + 2:
          # this is a sensor pair that shares an edge just out of range
          if self.sensors[i].pos.x == self.sensors[j].pos.x:
            point = Point(self.sensors[i].pos.x, (self.sensors[i].pos.y + self.sensors[j].pos.y) // 2)
            if not self._is_blocked(point):
              return point
          elif self.sensors[i].pos.y == self.sensors[j].pos.y:
            point = Point((self.sensors[i].pos.x + self.sensors[j].pos.x) // 2, self.sensors[i].pos.y)
            if not self._is_blocked(point):
              return point
          else:
            if self.sensors[i].radius <= self.sensors[j].radius:
              x_dir = (self.sensors[j].pos.x - self.sensors[i].pos.x) // abs(self.sensors[j].pos.x - self.sensors[i].pos.x)
              y_dir = (self.sensors[j].pos.y - self.sensors[i].pos.y) // abs(self.sensors[j].pos.y - self.sensors[i].pos.y)
              # count off the points.
              point = Point(
                self.sensors[i].pos.x + x_dir * (self.sensors[i].radius + 1),
                self.sensors[i].pos.y,
              )
              for _ in range(self.sensors[i].radius + 1):
                if (
                  manhattan_distance(self.sensors[j].pos, point) == self.sensors[j].radius + 1
                ) and (
                  not self._is_blocked(point)
                ):
                  return point
                else:
                  point = Point(
                    point.x - x_dir,
                    point.y + y_dir,
                  )
            else:
              x_dir = (self.sensors[i].pos.x - self.sensors[j].pos.x) // abs(self.sensors[i].pos.x - self.sensors[j].pos.x)
              y_dir = (self.sensors[i].pos.y - self.sensors[j].pos.y) // abs(self.sensors[i].pos.y - self.sensors[j].pos.y)
              # count off the points.
              point = Point(
                self.sensors[j].pos.x + x_dir * (self.sensors[j].radius + 1),
                self.sensors[j].pos.y,
              )
              for _ in range(self.sensors[j].radius + 1):
                if (
                  manhattan_distance(self.sensors[i].pos, point) == self.sensors[i].radius + 1
                ) and (
                  not self._is_blocked(point)
                ):
                  return point
                else:
                  point = Point(
                    point.x - x_dir,
                    point.y + y_dir,
                  )              