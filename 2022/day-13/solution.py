from __future__ import annotations
import json
import heapq
from enum import auto, Enum
from typing import List, Union
import itertools

from shared import SolutionABC

counter = itertools.count()

DIVIDER_PACKET_STRS = {
  '[[2]]',
  '[[6]]',
}

class Solution(SolutionABC):
  def __init__(
    self,
  ):
    self.packets: List[Packet] = [Packet(d_p_str) for d_p_str in DIVIDER_PACKET_STRS]
    heapq.heapify(self.packets)

  def parse_row(
    self,
    row: str,
  ):
    if len(row) != 0:
      heapq.heappush(self.packets, Packet(row))

  def solve(
    self,
  ) -> Union[int, str]:
    return self._prod_of_divider_packet_idxs()

  def _prod_of_divider_packet_idxs(
    self,
  ) -> int:
    idx = 1
    prod = 1
    while len(self.packets) > 0:
      packet = heapq.heappop(self.packets)
      if str(packet) in DIVIDER_PACKET_STRS:
        prod *= idx
      idx += 1
    return prod

class ComparisonResult(Enum):
  CORRECT = auto()
  INCONCLUSIVE = auto()
  INCORRECT = auto()

PacketData = Union[List[Union['PacketData', int]], int]

def compare(left: PacketData, right: PacketData) -> ComparisonResult:
  if isinstance(left, int) and isinstance(right, int):
    if left < right:
      return ComparisonResult.CORRECT
    elif left == right:
      return ComparisonResult.INCONCLUSIVE
    else:
      return ComparisonResult.INCORRECT
  elif isinstance(left, list) and isinstance(right, list):
    for i in range(len(left)):
      if len(right) <= i: return ComparisonResult.INCORRECT
      comp_res = compare(left[i], right[i])
      if comp_res != ComparisonResult.INCONCLUSIVE:
        return comp_res
    if len(right) == len(left):
      return ComparisonResult.INCONCLUSIVE
    else:
      return ComparisonResult.CORRECT
  else:
    if isinstance(left, list):
      assert isinstance(right, int)
      return compare(left, [right])
    else:
      assert isinstance(right, list) and isinstance(left, int)
      return compare([left], right)

class Packet:
  def __init__(
    self,
    row: str,
  ):
    self.data: PacketData = json.loads(row)
    self.counter: int = next(counter)

  def __lt__(self, other: Packet) -> bool:
    comp_res = compare(self.data, other.data)
    if comp_res == ComparisonResult.INCONCLUSIVE:
      return self.counter < other.counter
    else:
      return comp_res == ComparisonResult.CORRECT

  def __str__(self):
    return json.dumps(self.data)