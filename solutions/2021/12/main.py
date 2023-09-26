from __future__ import annotations
from collections import defaultdict
from typing import List

class Path:
  def __init__(self, steps: List[str]):
    self._steps = steps
    self._twice_visited_small_caves = set(
      filter(
        lambda step: step.islower() and steps.count(step) == 2,
        steps
      )
    )

  def is_valid_step(self, step: str) -> bool:
    if step == 'start':
      return False
    elif step.isupper() or step == 'end':
      return True
    else:
      assert step.islower()
      if step in self._steps and len(self._twice_visited_small_caves) == 1:
        return False
      else:
        return True

  def new_path(self, step: str) -> Path:
    assert self.is_valid_step(step)
    return Path(self._steps + [step])

  def most_recent_step(self) -> str:
    return self._steps[-1]

class CaveSystem:
  def __init__(self):
    self._connections = defaultdict(set)

  def add_connection(self, connection_str: str):
    start, end = connection_str.split('-')
    self._connections[start].add(end)
    self._connections[end].add(start)

  def _all_paths(self) -> List[Path]:
    valid_paths = []
    paths_being_explored = [Path(['start'])]
    while len(paths_being_explored) > 0:
      path = paths_being_explored.pop()
      for next_cave in self._connections[path.most_recent_step()]:
        if not path.is_valid_step(next_cave): continue
        if next_cave == 'end':
          valid_paths.append(
            path.new_path(next_cave)
          )
        else:
          paths_being_explored.append(
            path.new_path(next_cave)
          )
    return valid_paths

  def num_paths(self) -> int:
    return len(self._all_paths())

def parse_input(filename: str) -> CaveSystem:
  caves = CaveSystem()
  with open(filename) as f:
    for l in f:
      caves.add_connection(l.rstrip())
  return caves

if __name__ == '__main__':
  caves = parse_input('input/input.txt')
  print(caves.num_paths())