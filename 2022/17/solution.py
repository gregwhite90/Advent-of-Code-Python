from typing import Set, Dict, NamedTuple, DefaultDict, FrozenSet, List
from collections import defaultdict

from shared import SolutionABC

WIDTH = 7
START_X = 2
START_Y_DELTA = 3 # compared to height of tower
NUM_ROCKS = 1000000000000

class Point(NamedTuple):
  x: int
  y: int

ROCKS: Dict[int, Set[Point]] = {
  0: {
    Point(0, 0),
    Point(1, 0),
    Point(2, 0),
    Point(3, 0),
  },
  1: {
    Point(1, 0),
    Point(0, 1),
    Point(1, 1),
    Point(2, 1),
    Point(1, 2),
  },
  2: {
    Point(0, 0),
    Point(1, 0),
    Point(2, 0),
    Point(2, 1),
    Point(2, 2),
  },
  3: {
    Point(0, 0),
    Point(0, 1),
    Point(0, 2),
    Point(0, 3),
  },
  4: {
    Point(0, 0),
    Point(1, 0),
    Point(0, 1),
    Point(1, 1),
  },
}

class Rock:
  def __init__(self, idx: int, y: int):
    self.points: Set[Point] = ROCKS[idx]
    self.y: int = y
    self.x: int = START_X

  def absolute_points(self, x_shift: int = 0, y_shift: int = 0) -> Set[Point]:
    return set(
      Point(point.x + self.x + x_shift, point.y + self.y + y_shift) for point in self.points
    )

  def shift(self, x: int, y: int):
    self.x += x
    self.y += y

class PostTetrisStatus(NamedTuple):
  jet_index: int
  rock_index: int
  relative_blocked: FrozenSet[Point]

class TetrisResult(NamedTuple):
  y: int
  num_rocks: int

class Solution(SolutionABC):
  def __init__(
    self,
    jets: str = None,
    jet_index: int = 0,
    blocked: DefaultDict[int, Set[int]] = defaultdict(set),
    rock_index: int = 0,
    track_cyclicality: bool = True,
  ):
    self.jets: str = jets
    self.jet_index = jet_index
    self.blocked = blocked
    self.height: int = 0
    for y in self.blocked:
      self.height = max(self.height, y + 1)
    self.rock_index: int = rock_index
    self._previous_tetris_height: int = -1
    self._tetrises: DefaultDict[PostTetrisStatus, List[TetrisResult]] = defaultdict(list)
    self._rocks_simulated = 0
    self._track_cyclicality = track_cyclicality
    self.overall_solution: int = None

  def parse_row(
    self,
    row: str,
  ):
    self.jets = row

  def solve(
    self,
  ) -> int:
    while self.overall_solution is None:
      self._simulate_next_rock()
    return self.overall_solution

  def __str__(self) -> str:
    res = '+' + '-' * WIDTH + '+'
    for y in range(self.height):
      row = '|'
      for x in range(WIDTH):
        row += ('#' if x in self.blocked[y] else '.')       
      row += '|\n'
      res = row + res
    return res

  def partial_to_str(self, y: int, buffer: int = 2) -> str:
    res = ''
    for y in range(y - buffer, y + buffer + 1):
      row = '|'
      for x in range(WIDTH):
        row += ('#' if x in self.blocked[y] else '.')       
      row += '|\n'
      res = row + res
    return res

  def _simulate_n_rocks(self, n: int = 2022):
    for _ in range(n):
      self._simulate_next_rock()

  def _simulate_next_rock(self):
    rock = Rock(self.rock_index, self.height + START_Y_DELTA)
    self.rock_index = (self.rock_index + 1) % len(ROCKS)
    while True:
      jet = self.jets[self.jet_index]
      self.jet_index = (self.jet_index + 1) % len(self.jets)
      x_shift = 1 if jet == '>' else -1
      if not self._rock_is_blocked(rock, x_shift, 0):
        rock.shift(x_shift, 0)
      if not self._rock_is_blocked(rock, 0, -1):
        rock.shift(0, -1)
      else:
        tetris_ys = []
        for point in rock.absolute_points():
          self.blocked[point.y].add(point.x)
          self.height = max(self.height, point.y + 1)
          if len(self.blocked[point.y]) == WIDTH:
            tetris_ys.append(point.y)
        self._rocks_simulated += 1
        for y in tetris_ys:
          self._record_tetris(y)
        break

  def _record_tetris(self, y: int):
    for i in range(y - 1, self._previous_tetris_height - 1, -1):
      self.blocked.pop(i, None)
    self._previous_tetris_height = y
    if self._track_cyclicality:
      relative_blocked = set()
      for pt_y in self.blocked:
        for pt_x in self.blocked[pt_y]:
          relative_blocked.add(Point(pt_x, pt_y - y))
      relative_blocked = frozenset(relative_blocked)
      pts = PostTetrisStatus(
        self.jet_index, 
        self.rock_index,
        relative_blocked,
      )
      self._tetrises[pts].append(TetrisResult(
        y,
        self._rocks_simulated,
      ))
      if len(
        self._tetrises[pts]
      ) == 3:
        tetris_results = self._tetrises[pts]
        assert tetris_results[2].y - tetris_results[1].y == tetris_results[1].y - tetris_results[0].y
        assert tetris_results[2].num_rocks - tetris_results[1].num_rocks == tetris_results[1].num_rocks - tetris_results[0].num_rocks
        rocks_remaining = NUM_ROCKS - tetris_results[0].num_rocks
        rocks_per_cycle = tetris_results[1].num_rocks - tetris_results[0].num_rocks
        cycles = rocks_remaining // rocks_per_cycle
        rocks_after_cycles = rocks_remaining % rocks_per_cycle
        base_y = tetris_results[0].y + cycles * (tetris_results[1].y - tetris_results[0].y)
        blocked: DefaultDict[int, Set[int]] = defaultdict(set)
        for point in pts.relative_blocked:
          blocked[point.y].add(point.x)
        new_soln = Solution(
          jets=self.jets,
          jet_index=pts.jet_index,
          blocked=blocked,
          rock_index=pts.rock_index,
          track_cyclicality=False,
        )
        new_soln._simulate_n_rocks(n=rocks_after_cycles)
        self.overall_solution = base_y + new_soln._height()

  def _height(self) -> int:
    return self.height

  def _rock_is_blocked(self, rock: Rock, x_shift: int, y_shift: int) -> bool:
    for point in rock.absolute_points(x_shift=x_shift, y_shift=y_shift):
      if (
        point.y < 0
      ) or (
        point.x < 0
      ) or (
        point.x >= WIDTH
      ) or (
        point.x in self.blocked[point.y]
      ):
        return True
    return False