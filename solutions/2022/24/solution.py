from __future__ import annotations
import heapq
import re
import itertools
import math
from typing import NamedTuple, DefaultDict, Set
from collections import defaultdict

from solutions.shared import SolutionABC

WALL_RE = re.compile(r"\#+\.\#+")

counter = itertools.count()

class Point(NamedTuple):
  x: int
  y: int

class Plan:
  def __init__(
    self,
    minutes: int,
    point: Point,
  ):
    self.minutes = minutes
    self.point = point
    self.counter = next(counter)

  def __lt__(self, other: Plan) -> bool:
    if self.minutes != other.minutes:
      return self.minutes < other.minutes
    elif self.point.x + self.point.y != other.point.x + other.point.y:
      return self.point.x + self.point.y > other.point.x + other.point.y
    else:
      return self.counter < other.counter

class Solution(SolutionABC):
  def __init__(
    self,
  ):
    self._blocked_horizontally: DefaultDict[Point, Set[int]] = defaultdict(set)
    self._blocked_vertically: DefaultDict[Point, Set[int]] = defaultdict(set)
    self._downs: DefaultDict[int, Set[int]] = defaultdict(set)
    self._ups: DefaultDict[int, Set[int]] = defaultdict(set)
    self.rows = 0
    self.cols = None

  def parse_row(
    self,
    row: str,
  ):
    if WALL_RE.match(row):
      if self.rows == 0:
        self.start = Point(row.index('.') - 1, -1)
      else:
        self.end = Point(row.index('.') - 1, self.rows)
        self._calculate_blocked_vertically()
    else:
      self.parse_field_row(row)
    
  def parse_field_row(
    self,
    row: str,
  ):
    assert row [0] == '#' and row[-1] == '#'
    if self.cols is None:
      self.cols = len(row) - 2
    assert self.cols == len(row) - 2
    for col, char in enumerate(row[1 : -1]):
      if char == '^':
        self._ups[col].add(self.rows)
      elif char == 'v':
        self._downs[col].add(self.rows)
      if char != '>' and char != '<':
        continue
      for x in range(self.cols):
        if char == '>':
          self._blocked_horizontally[Point(x, self.rows)].add(
            (x - col) % self.cols
          )
        elif char == '<':
          self._blocked_horizontally[Point(x, self.rows)].add(
            (col - x) % self.cols
          )
    self.rows += 1

  def solve(
    self,
  ) -> int:
    first_mins = self._optimal_time(0, self.start, self.end)
    second_mins = self._optimal_time(first_mins, self.end, self.start)
    third_mins = self._optimal_time(second_mins, self.start, self.end)
    return third_mins

  def _optimal_time(
    self,
    start_minutes: int,
    start: Point,
    end: Point,
  ) -> int:
    explored: DefaultDict[Point, Set[int]] = defaultdict(set)
    pq = [Plan(start_minutes, start)]
    while True:
      cur = heapq.heappop(pq)
      if cur.point == end:
        return cur.minutes
      if cur.minutes % (self.rows * self.cols // math.gcd(self.rows, self.cols)) in explored[cur.point]:
        continue
      explored[cur.point].add(cur.minutes % (self.rows * self.cols // math.gcd(self.rows, self.cols)))
      for next_pt in self._options(cur, explored):
        heapq.heappush(pq, Plan(cur.minutes + 1, next_pt))

  def _calculate_blocked_vertically(self):
    for col in range(self.cols):
      for y in range(self.rows):
        for row in self._ups[col]:
          self._blocked_vertically[Point(col, y)].add(
            (row - y) % self.rows
          )
        for row in self._downs[col]:
         self._blocked_vertically[Point(col, y)].add(
           (y - row) % self.rows
         )
    
  def _options(
    self,
    plan: Plan,
    explored: DefaultDict[Point, Set[int]],
  ) -> Set[Point]:
    pt: Point = plan.point
    mins: int = plan.minutes
    res = set()
    potential_pts = [
      pt,
    ]
    if pt != self.start and pt != self.end and pt.x < self.cols - 1:
      potential_pts.append(Point(pt.x + 1, pt.y))
    if pt != self.start and pt != self.end and pt.x > 0:
      potential_pts.append(Point(pt.x - 1, pt.y))
    if pt.y < self.rows - 1 or Point(pt.x, pt.y + 1) == self.end:
      potential_pts.append(Point(pt.x, pt.y + 1))
    if pt.y > 0 or Point(pt.x, pt.y - 1) == self.start:
      potential_pts.append(Point(pt.x, pt.y - 1))
    for potential_pt in potential_pts:
      if self._open(potential_pt, mins + 1) and (mins + 1) % ((self.cols * self.rows) // math.gcd(self.cols, self.rows)) not in explored[pt]:
        res.add(potential_pt)
    return res

  def _open(
    self,
    point: Point,
    minutes: int,
  ) -> bool:
    return minutes % self.cols not in self._blocked_horizontally[point] and minutes % self.rows not in self._blocked_vertically[point]