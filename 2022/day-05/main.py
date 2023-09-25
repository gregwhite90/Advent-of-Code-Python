import re
from collections import deque

ROW_RE = re.compile(
  r"( *)\[([A-Z])\] ?"
)
MOVE_RE = re.compile(
  r"move (?P<num>\d+) from (?P<origin>\d+) to (?P<dest>\d+)"
)

class Stacks:
  def __init__(self, num_stacks: int = 9):
    self._stacks = [deque() for _ in range(num_stacks)]

  def add_row(self, row: str):
    matches = ROW_RE.findall(row)
    assert matches
    idx = 0
    for whitespace, letter in matches:
      idx += len(whitespace) // 4
      self._stacks[idx].appendleft(letter)
      idx += 1

  def move(self, row: str):
    match = MOVE_RE.match(row)
    assert match
    num = int(match['num'])
    origin = int(match['origin']) - 1
    dest = int(match['dest']) - 1
    temp_stack = deque()
    for _ in range(num):
      item = self._stacks[origin].pop()
      temp_stack.append(item)
    for _ in range(num):
      item = temp_stack.pop()
      self._stacks[dest].append(item)

  def tops(self) -> str:
    return ''.join(
      stack[-1] for stack in self._stacks
    )

def parse_input(filename: str, num_stacks: int = 9) -> Stacks:
  stacks = Stacks(num_stacks = num_stacks)
  with open(filename) as f:
    for l in f:
      if ROW_RE.findall(l):
        stacks.add_row(l)
      elif MOVE_RE.match(l):
        stacks.move(l)
  return stacks

if __name__ == '__main__':
  stacks = parse_input('input.txt')
  print(stacks.tops())