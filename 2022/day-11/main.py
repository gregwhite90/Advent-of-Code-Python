from __future__ import annotations
import re
import math
from collections import deque
from enum import Enum
from typing import Deque, List, NamedTuple

MONKEY_RE = re.compile(r"Monkey (?P<id>\d+):")
ITEMS_RE = re.compile(r"  Starting items: (?P<items>[ \,\d]+)")
OPERATION_RE = re.compile(r"  Operation: new = old (?P<operation>[\+\*]) (?P<operand>old|\d+)")
TEST_RE = re.compile(r"  Test: divisible by (?P<denominator>\d+)")
RECIPIENT_RE = re.compile(r"    If (?P<result>true|false): throw to monkey (?P<recipient>\d+)")

class Operation(Enum):
  ADD = '+'
  MULTIPLY = '*'

class Throw(NamedTuple):
  item: int
  recipient: int

class Monkey:
  def __init__(self):
    self._items: Deque[int] = None
    self._operation: Operation = None
    self._operand: int | str = None
    self._denominator: int = None
    self._recipient_if_t = None
    self._recipient_if_f = None
    self._items_inspected = 0

  def parse_row(self, row: str):
    if ITEMS_RE.match(row):
      m = ITEMS_RE.match(row)
      self._items = deque(int(item) for item in m['items'].split(', '))
    elif TEST_RE.match(row):
      m = TEST_RE.match(row)
      self._denominator = int(m['denominator'])
    elif OPERATION_RE.match(row):
      m = OPERATION_RE.match(row)
      self._operation = Operation(m['operation'])
      self._operand = m['operand'] if m['operand'] == 'old' else int(m['operand'])
    elif RECIPIENT_RE.match(row):
      m = RECIPIENT_RE.match(row)
      if m['result'] == 'true':
        self._recipient_if_t = int(m['recipient'])
      else:
        assert m['result'] == 'false'
        self._recipient_if_f = int(m['recipient'])
    else:
      raise Exception(f"Unrecognized row: {row}")

  def num_items(self) -> int:
    return len(self._items)

  def add_item(self, item: int):
    self._items.append(item)

  def inspect(self, denominator: int) -> Throw:
    assert self.num_items() > 0
    self._items_inspected += 1
    item = self._item_after_inspection(self._items.popleft(), denominator)
    if item % self._denominator == 0:
      return Throw(item, self._recipient_if_t)
    else:
      return Throw(item, self._recipient_if_f)

  def _item_after_inspection(self, old: int, denominator: int) -> int:
    new = old
    if self._operation == Operation.ADD:
      if self._operand == 'old':
        new += old
      else:
        new += self._operand
    else:
      assert self._operation == Operation.MULTIPLY
      if self._operand == 'old':
        new *= old
      else:
        new *= self._operand
    return new % denominator

  def items_inspected(self) -> int:
    return self._items_inspected

  def denominator(self) -> int:
    return self._denominator

class Monkeys:
  def __init__(self):
    self._monkeys: List[Monkey] = []
    self._denominator: int = None

  def parse_row(self, row: str):
    if len(row) == 0:
      return
    elif MONKEY_RE.match(row):
      m = MONKEY_RE.match(row)
      assert len(self._monkeys) == int(m['id'])
      self._monkeys.append(Monkey())
    else:
      self._monkeys[-1].parse_row(row)

  def simulate_rounds(self, rounds: int = 10000):
    for _ in range(rounds):
      self._simulate_round()        

  def _simulate_round(self):
    if not self._denominator:
      self._denominator = math.prod(monkey.denominator() for monkey in self._monkeys)
    for id in range(len(self._monkeys)):
      while self._monkeys[id].num_items() > 0:
        throw = self._monkeys[id].inspect(self._denominator)
        self._monkeys[throw.recipient].add_item(throw.item)

  def monkey_business(self, num_monkeys: int = 2) -> int:
    inspected = [monkey.items_inspected() for monkey in self._monkeys]
    inspected.sort(reverse = True)
    return math.prod(inspected[ : num_monkeys])

def parse_input(filename: str) -> Monkeys:
  monkeys = Monkeys()
  with open(filename) as f:
    for l in f:
      monkeys.parse_row(l.rstrip())
  return monkeys

if __name__ == '__main__':
  monkeys = parse_input('input.txt')
  monkeys.simulate_rounds()
  print(monkeys.monkey_business())