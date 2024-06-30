from typing import List, NamedTuple, Dict, Set, FrozenSet, Tuple
from collections import defaultdict

from solutions.shared import SolutionABC, IntcodeComputer, InputMode
from solutions.shared.utils import print_solution

import heapq

"""
First pass: simple BFS. prune if same position with same set of keys with >= steps.
Possible efficiency improvement: track the distance and doors between each pairwise set of keys.

heapq.

start_to_key: key and dist, no doors.
key_to_key: {2 keys}, dist, set of doors.

"""

class Position(NamedTuple):
  x: int
  y: int

def adjacent_positions(pos: Position) -> List[Position]:
  return [
    Position(pos.x + x_offset, pos.y + y_offset)
    for x_offset, y_offset
    in [(0, 1), (0, -1), (1, 0), (-1, 0)]
  ]

class Maze:
  def __init__(self):
    self.walls: Set[Position] = set()
    self.keys: Dict[Position, str] = dict()
    self.doors: Dict[Position, str] = dict()
    self.start: Position = None
    self.row: int = 0

  def parse_row(
    self,
    row: str
  ):    
    for i, ch in enumerate(row):
      if ch == '.': continue
      pos = Position(i, self.row)
      match ch:
        case '@':
          self.start = pos
        case '#':
          self.walls.add(pos)
        case _:
          if ch.isupper():
            self.doors[pos] = ch
          else:
            assert(ch.islower())
            self.keys[pos] = ch
    self.row += 1
      
class AccessPath:
  def __init__(
    self,
    steps: int,
    doors: Set[str],
  ):
    self.steps = steps
    self.doors = doors

class VaultPath:
  def __init__(
    self,
    start: str,
    position: Position,
    doors: Set[str],
    steps: int = 0,
  ):
    self.start = start
    self.steps = steps
    self.position = position
    self.doors = doors

  def __lt__(self, other):
    return self.steps < other.steps

class VaultSearcher:
  def __init__(self, maze: Maze):
    self.start_to_key: Dict[str, AccessPath] = dict()
    self.key_to_key: Dict[FrozenSet[str], AccessPath] = dict()
    pq = []
    heapq.heappush(pq, VaultPath('@', maze.start, set()))
    start_to_visited: Dict[str, Set[Position]] = defaultdict(set)
    while pq:
      path = heapq.heappop(pq)
      if path.position in start_to_visited[path.start]: continue
      start_to_visited[path.start].add(path.position)
      if path.position in maze.keys and path.steps != 0:
        if path.start == '@':
          self.start_to_key[maze.keys[path.position]] = AccessPath(path.steps, path.doors.copy())
        else:
          self.key_to_key[frozenset({path.start, maze.keys[path.position]})] = AccessPath(path.steps, path.doors.copy())
        heapq.heappush(
          pq, 
          VaultPath(maze.keys[path.position], path.position, set())
        )
      elif path.position in maze.doors:
        path.doors.add(maze.doors[path.position])
      for adj in adjacent_positions(path.position):
        if adj not in start_to_visited[path.start] and adj not in maze.walls:
          heapq.heappush(
            pq,
            VaultPath(
              path.start,
              adj,
              path.doors.copy(),
              steps=path.steps + 1,
            )
          )
  
  def min_steps(self) -> int:
    all_keys = set(self.start_to_key.keys())
    for keys in self.key_to_key.keys():
      all_keys |= keys
    pq = []
    # Visited is the current position and the collected keys
    visited: Set[Tuple[str, FrozenSet[str]]] = set()
    for key, ap in self.start_to_key.items():
      if len(ap.doors) != 0: continue
      heapq.heappush(pq, VaultSearcherPath(ap.steps, key, {key}, all_keys.copy() - {key}))
    while pq:
      path = heapq.heappop(pq)
      if len(path.keys_uncollected) == 0:
        return path.steps
      if (path.key, frozenset(path.keys_collected)) in visited: continue
      visited.add((path.key, frozenset(path.keys_collected)))
      for keys, ap in self.key_to_key.items():
        if path.key not in keys or len(ap.doors - {k.upper() for k in path.keys_collected}) != 0: continue
        new_key = None
        for key in keys:
          if key != path.key: new_key = key
        if new_key in path.keys_collected: continue
        heapq.heappush(
          pq,
          VaultSearcherPath(
            path.steps + ap.steps,
            new_key,
            path.keys_collected.copy() | {new_key},
            path.keys_uncollected.copy() - {new_key},
          ),
        )

class VaultSearcherPath:
  def __init__(
      self,
      steps: int,
      key: str,
      keys_collected: Set[str],
      keys_uncollected: Set[str],
  ):
    self.steps = steps
    self.key = key
    self.keys_collected = keys_collected
    self.keys_uncollected = keys_uncollected
    
  def __lt__(self, other):
    return self.steps < other.steps

class Solution(SolutionABC):
  def __init__(
    self,
  ):
    self.maze = Maze()
    self.vault_searcher: VaultSearcher = None

  def parse_row(
    self,
    row: str,
  ):
    self.maze.parse_row(row)

  def solve(
    self,
  ) -> int:
    self.vault_searcher = VaultSearcher(self.maze)
    return self.vault_searcher.min_steps()

if __name__ == '__main__':
  soln = Solution()
  print_solution(soln, ['2019', '18'])