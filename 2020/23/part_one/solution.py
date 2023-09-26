from __future__ import annotations
from typing import Set

from shared import SolutionABC

PICKUPS = 3
MOVES = 100

class Node:
  """
  A node in a doubly linked list
  """
  def __init__(self, value: int, prev: Node):
    self.value: int = value
    self.prev: Node = prev
    self.next: Node = None

class Solution(SolutionABC):
  def __init__(
    self,
  ):
    self.head: Node = None
    self.cur: Node = None
    self.length: int = 0

  def parse_row(
    self,
    row: str,
  ):
    # construct the doubly linked list
    self.length = len(row)
    for i, char in enumerate(row):
      if i == 0:
        self.head = Node(int(char) - 1, None)
        cur = self.head
      else:
        node = Node(int(char) - 1, cur)
        cur.next = node
        cur = node
    # close the loop
    cur.next = self.head
    self.head.prev = cur
    # set up for the game
    self.cur = self.head

  def _move(self):
    values_picked_up: Set[int] = set()
    pickup_head = self.cur.next
    pickup_cur = pickup_head
    for _ in range(PICKUPS):
      values_picked_up.add(pickup_cur.value)
      pickup_cur = pickup_cur.next
    pickup_cur = pickup_cur.prev
    
    # splice out the pickups
    pickup_head.prev = None
    pickup_cur.next.prev = self.cur
    self.cur.next = pickup_cur.next
    pickup_cur.next = None

    # find the destination
    dest_value = (self.cur.value - 1) % self.length
    while dest_value in values_picked_up:
      dest_value = (dest_value - 1) % self.length

    dest_node = self.cur.next
    val = dest_node.value
    while val != dest_value:
      dest_node = dest_node.next
      val = dest_node.value
    # splice back in the pickups
    right_node = dest_node.next
    dest_node.next = pickup_head
    pickup_head.prev = dest_node
    pickup_cur.next = right_node
    right_node.prev = pickup_cur

    # advance current cup
    self.cur = self.cur.next

  def _labels_after_1(self) -> str:
    res = ''
    # find the 1 value (re-indexed to 0 internally for mod math)
    cur = self.head
    val = cur.value
    while val != 0:
      cur = cur.next
      val = cur.value
    cur = cur.next
    val = cur.value
    while val != 0:
      res += str(val + 1)
      cur = cur.next
      val = cur.value
    return res

  def solve(
    self,
  ) -> int:
    for _ in range(MOVES):
      self._move()
    return self._labels_after_1()