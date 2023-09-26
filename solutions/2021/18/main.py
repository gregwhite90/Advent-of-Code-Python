from __future__ import annotations
from typing import List
import itertools

class SnailfishNumber:
  def __init__(
    self,
    parent: SnailfishNumber,
    index_in_parent: int,
    remaining: str,
  ):
    assert remaining[0] == '['
    self.parent = parent
    self.index_in_parent = index_in_parent
    self.elements: List[SnailfishNumber | int] = []
    idx = 1
    for iter, end_char in enumerate([',', ']']):
      if remaining[idx] == '[':
        sn = SnailfishNumber(self, iter, remaining[idx : ])
        self.elements.append(sn)
        idx += sn.str_len
      else:
        orig_idx = idx
        while remaining[idx] != end_char:
          idx += 1
        self.elements.append(int(remaining[orig_idx : idx]))
      assert remaining[idx] == end_char
      idx += 1
    self.str_len = idx
    assert len(self.elements) == 2
    self._max_depth: int = None
    self.update_max_depth()
    self._max_num: int = None
    self.update_max_num()
    
  def update_max_depth(self):
    if len(self.elements) != 2: return
    max_depth = max(
      0 if isinstance(el, int) else el.max_depth() for el in self.elements
    ) + 1
    if max_depth != self._max_depth:
      self._max_depth = max_depth
      if self.parent:
        self.parent.update_max_depth()

  def max_depth(self):
    return self._max_depth

  def update_max_num(self):
    if len(self.elements) != 2: return
    max_num = max(
      el if isinstance(el, int) else el.max_num() for el in self.elements
    )
    if max_num != self._max_num:
      self._max_num = max_num
      if self.parent:
        self.parent.update_max_num()

  def max_num(self):
    return self._max_num

  def reduce(self):
    while self.max_depth() > 4 or self.max_num() >= 10:
      if self.max_depth() > 4:
        self.explode()
      else:
        assert self.max_num() >= 10
        self.split()

  def explode(self, depth: int = 0):
    assert self.max_depth() + depth > 4
    if depth == 4:
      assert self.max_depth() == 1 and isinstance(self.elements[0], int) and isinstance(self.elements[1], int)
      self._traverse(1)
      self._traverse(0)          
      self.parent.elements[self.index_in_parent] = 0
      self.parent.update_max_depth()
      self.parent.update_max_num()
    else:
      if isinstance(self.elements[0], SnailfishNumber) and depth + 1 + self.elements[0].max_depth() > 4:
        self.elements[0].explode(depth = depth + 1)
      else:
        assert isinstance(self.elements[1], SnailfishNumber) and depth + 1 + self.elements[1].max_depth() > 4
        self.elements[1].explode(depth = depth + 1)

  def _traverse(self, idx_sought: int):
    idx: int = self.index_in_parent
    node: SnailfishNumber = self.parent
    while idx == 1 - idx_sought:
      idx = node.index_in_parent
      node = node.parent
    if idx == idx_sought:
      assert node
      if isinstance(node.elements[1 - idx_sought], int):
        node.elements[1 - idx_sought] += self.elements[1 - idx_sought]
      else:
        node = node.elements[1 - idx_sought]
        while not isinstance(node.elements[idx_sought], int):
          node = node.elements[idx_sought]
        node.elements[idx_sought] += self.elements[1 - idx_sought]
      node.update_max_depth()
      node.update_max_num()

  def split(self):
    if isinstance(self.elements[0], int) and self.elements[0] >= 10:
      self._split_element(0)
    elif isinstance(self.elements[0], SnailfishNumber) and self.elements[0].max_num() >= 10:
      self.elements[0].split()
    elif isinstance(self.elements[1], int) and self.elements[1] >= 10:
      self._split_element(1)      
    else:      
      assert isinstance(self.elements[1], SnailfishNumber) and self.elements[1].max_num() >= 10
      self.elements[1].split()

  def _split_element(self, idx: int):
    assert isinstance(self.elements[idx], int) and self.elements[idx] >= 10
    l = self.elements[idx] // 2
    r = self.elements[idx] // 2 + self.elements[idx] % 2
    self.elements[idx] = SnailfishNumber(self, idx, f"[{l},{r}]")
    self.update_max_depth()
    self.update_max_num()
  
  def __str__(self):
    return '[' + ','.join(str(el) for el in self.elements) + ']'

  def __add__(self, other: SnailfishNumber) -> SnailfishNumber:
    remaining: str = '[' + ','.join([str(self), str(other)]) +']'
    sn = SnailfishNumber(None, None, remaining)
    sn.reduce()
    return sn

  def magnitude(self) -> int:
    return (
      3 * (self.elements[0] if isinstance(self.elements[0], int) else self.elements[0].magnitude()) +
      2 * (self.elements[1] if isinstance(self.elements[1], int) else self.elements[1].magnitude())
    )

def parse_input(filename: str) -> List[SnailfishNumber]:
  with open(filename) as f:
    sn = [SnailfishNumber(None, None, l.rstrip()) for l in f.readlines()]
  return sn

def largest_magnitude(sns: List[SnailfishNumber]) -> int:
  l_m = 0
  for l, r in itertools.product(range(len(sns)), repeat=2):
    if l != r:
      new = sns[l] + sns[r]
      mag = new.magnitude()
      if mag > l_m: l_m = mag
  return l_m

if __name__ == '__main__':
  sns = parse_input('input/input.txt')
  print(largest_magnitude(sns))