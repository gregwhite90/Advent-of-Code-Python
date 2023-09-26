"""
Used https://www.reddit.com/r/adventofcode/comments/kimluc/comment/ggse107/ to figure out the lookup list data structure approach.
"""
from typing import List, Set

from shared import SolutionABC

class Solution(SolutionABC):
  def __init__(
    self,
  ):
    # singly-linked-list like data structure. tracks the index of the cup to the right.
    self.right_idx: List[int] = None

    self.cups: List[int] = None
    self.head: int = None

  def parse_row(
    self,
    row: str,
  ):
    self.cups = list(map(int, row))
    self.head = self.cups[0]

  def _labels_after_1(
    self,
    moves: int,
    pad_to_length: int,
  ):
    self.right_idx = [i + 1 for i in range(pad_to_length + 1)]

    # update for starting cup arrangement
    for i, cup in enumerate(self.cups[:-1]):
      self.right_idx[cup] = self.cups[i + 1]

    # close the linked list
    if pad_to_length > len(self.cups):
      self.right_idx[self.cups[-1]] = max(self.cups) + 1
      self.right_idx[-1] = self.head
    else:
      self.right_idx[self.cups[-1]] = self.head

    for _ in range(moves):
      pickup_head = self.right_idx[self.head]
      self.right_idx[self.head] = self.right_idx[self.right_idx[self.right_idx[pickup_head]]]
      
      picked_up: Set[int] = {pickup_head, self.right_idx[pickup_head], self.right_idx[self.right_idx[pickup_head]]}
      
      dest = self.head - 1 if self.head > 1 else pad_to_length
      while dest in picked_up:
        dest = pad_to_length if dest == 1 else dest - 1

      self.right_idx[self.right_idx[self.right_idx[pickup_head]]] = self.right_idx[dest]
      self.right_idx[dest] = pickup_head

      self.head = self.right_idx[self.head]

    cup = self.right_idx[1]
    while cup != 1:
      yield cup
      cup = self.right_idx[cup]

  def solve(
    self,
  ) -> int:
    labels_iter = self._labels_after_1(10000000, 1000000)
    return next(labels_iter) * next(labels_iter)