from __future__ import annotations
from typing import Union, List

from shared import SolutionABC

DECRYPTION_KEY = 811589153

class Element:
  def __init__(self, row: str, prev: Element):
    self.times_mixed = 0
    self.number = int(row) * DECRYPTION_KEY
    self.orig_next: Element = None
    self.cur_next: Element = None
    self.orig_prev: Element = prev
    self.cur_prev: Element = prev

class CircularList:
  def __init__(self):
    self.times_mixed = 0
    self.most_recent: Element = None
    self.orig_head: Element = None
    self.num_elements = 0
    self.circle_closed = False

  def add_row(self, row: str):
    self.num_elements += 1
    new = Element(row, self.most_recent)
    if self.orig_head is None:
      self.orig_head = new
    if self.most_recent is not None:
      self.most_recent.orig_next = new
      self.most_recent.cur_next = new
    self.most_recent = new

  def close_circle(self):
    if not self.circle_closed:
      assert self.orig_head is not None and self.most_recent is not None
      self.orig_head.orig_prev = self.most_recent
      self.orig_head.cur_prev = self.most_recent
      self.most_recent.orig_next = self.orig_head
      self.most_recent.cur_next = self.orig_head
      self.circle_closed = True

  def mix(self):
    assert self.circle_closed
    nums_mixed = 0
    cur_being_mixed = self.orig_head
    while nums_mixed < self.num_elements:
      if cur_being_mixed.times_mixed > self.times_mixed:
        cur_being_mixed = cur_being_mixed.orig_next
        continue
      cur_being_mixed.times_mixed += 1
      nums_mixed += 1
      locn = cur_being_mixed.cur_prev
      moves = cur_being_mixed.number % (self.num_elements - 1)
      self._excise_elem(cur_being_mixed)
      for _ in range(moves):
        locn = locn.cur_next
      self._insert_elem_right_of_locn(cur_being_mixed, locn)
      cur_being_mixed = cur_being_mixed.orig_next
    self.times_mixed += 1

  def mix_n_times(self, n: int = 10):
    for _ in range(n):
      self.mix()

  def _excise_elem(self, elem: Element):
    elem.cur_next.cur_prev = elem.cur_prev
    elem.cur_prev.cur_next = elem.cur_next
    elem.cur_next = None
    elem.cur_prev = None

  def _insert_elem_right_of_locn(self, elem: Element, locn: Element):
    elem.cur_prev = locn
    elem.cur_next = locn.cur_next
    locn.cur_next.cur_prev = elem
    locn.cur_next = elem

  def sum_coordinates(self) -> int:
    res = 0
    cur = self.orig_head
    while cur.number != 0:
      cur = cur.cur_next
    for _ in range(3):
      for _ in range(1000):
        cur = cur.cur_next
      res += cur.number
    return res

  def _to_list(self) -> List[int]:
    cur = self.orig_head
    res = [cur.number]
    for _ in range(self.num_elements - 1):
      cur = cur.cur_next
      res.append(cur.number)
    return res    

  def __str__(self) -> str:
    return str(self._to_list())

class Solution(SolutionABC):
  def __init__(
    self,
  ):
    self.cl = CircularList()

  def parse_row(
    self,
    row: str,
  ):
    self.cl.add_row(row)

  def solve(
    self,
  ) -> Union[int, str]:
    self.cl.close_circle()
    self.cl.mix_n_times(n=10)
    return self.cl.sum_coordinates()