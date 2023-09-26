import itertools
from typing import Set, DefaultDict, List, NamedTuple
from collections import defaultdict
from enum import Enum

from shared import SolutionABC

class Point(NamedTuple):
  x: int
  y: int

class Direction(Enum):
  NORTH = 0
  SOUTH = 1
  WEST = 2
  EAST = 3

def all_adjacent(pt: Point) -> Set[Point]:
  res = set()
  for x, y in itertools.product(
    [pt.x - 1, pt.x, pt.x + 1],
    [pt.y - 1, pt.y, pt.y + 1],
  ):
    if x != pt.x or y != pt.y:
      res.add(Point(x, y))
  return res

def adjacent_in_direction(pt: Point, dir: Direction) -> Set[Point]:
  res = set()
  for offset in [-1, 0, 1]:
    if dir == Direction.NORTH:
      res.add(Point(pt.x + offset, pt.y - 1))
    elif dir == Direction.SOUTH:
      res.add(Point(pt.x + offset, pt.y + 1))
    elif dir == Direction.EAST:
      res.add(Point(pt.x + 1, pt.y + offset))
    else:
      assert dir == Direction.WEST
      res.add(Point(pt.x - 1, pt.y + offset))
  return res

def proposed_move(pt: Point, dir: Direction) -> Point:
  if dir == Direction.NORTH:
    return Point(pt.x, pt.y - 1)
  elif dir == Direction.SOUTH:
    return Point(pt.x, pt.y + 1)
  elif dir == Direction.EAST:
    return Point(pt.x + 1, pt.y)
  else:
    assert dir == Direction.WEST
    return Point(pt.x - 1, pt.y)

class Solution(SolutionABC):
  def __init__(
    self,
  ):
    self.elves: Set[Point] = set()
    self.rows = 0
    self.rounds = 0

  def parse_row(
    self,
    row: str,
  ):
    for col, char in enumerate(row):
      if char == '#':
        self.elves.add(Point(col, self.rows))
    self.rows += 1

  def solve(
    self,
  ) -> int:
    while True:
      if self._simulate_round():
        break
    return self.rounds

  def _simulate_round(self) -> bool:
    proposed_moves = self._propose_moves()
    moves_executed = self._execute_moves(proposed_moves)
    self.rounds += 1
    return moves_executed == 0

  def _propose_moves(self) -> DefaultDict[Point, List[Point]]:
    proposed_moves: DefaultDict[Point, List[Point]] = defaultdict(list)
    for elf in self.elves:
      if len(all_adjacent(elf).intersection(self.elves)) == 0:
        continue
      for attempt in range(len(Direction)):
        direction = Direction((self.rounds + attempt) % len(Direction))
        if len(adjacent_in_direction(elf, direction).intersection(self.elves)) == 0:
          proposed_moves[proposed_move(elf, direction)].append(elf)
          break
    return proposed_moves

  def _execute_moves(self, proposed_moves: DefaultDict[Point, List[Point]]) -> int:
    moves_executed = 0
    for new_pt, elves in proposed_moves.items():
      if len(elves) == 1:
        self.elves.remove(elves[0])
        self.elves.add(new_pt)
        moves_executed += 1
    return moves_executed

  def _num_empty_in_bounding_box(self) -> int:
    max_x = max(elf.x for elf in self.elves)
    min_x = min(elf.x for elf in self.elves)
    max_y = max(elf.y for elf in self.elves)
    min_y = min(elf.y for elf in self.elves)
    return (max_x - min_x + 1) * (max_y - min_y + 1) - len(self.elves)