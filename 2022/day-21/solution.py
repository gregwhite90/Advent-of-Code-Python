from __future__ import annotations
import re
from typing import Union, Dict
from enum import Enum, auto

from shared import SolutionABC

NUM_RE = re.compile(r"(?P<id>[a-z]{4}): (?P<num>\d+)")
OP_RE = re.compile(r"(?P<id>[a-z]{4}): (?P<l_operand>[a-z]{4}) (?P<operation>[\+\/\*\-]) (?P<r_operand>[a-z]{4})")

class Operation(Enum):
  ADD = '+'
  DIVIDE = '/'
  MULTIPLY = '*'
  SUBTRACT = '-'

class MonkeyType(Enum):
  NUMBER = auto()
  OPERATION = auto()
  HUMAN = auto()
  ROOT = auto()

class ValueType(Enum):
  KNOWN = auto()
  DEPENDENT = auto()

class Monkey:
  def __init__(self, row: str):
    self._value = None
    m = NUM_RE.match(row)
    if m:
      self.type = MonkeyType.NUMBER
      self.num = int(m['num'])
    else:
      m = OP_RE.match(row)
      assert m
      self.type = MonkeyType.OPERATION
      self.l_operand = m['l_operand']
      self.operation = Operation(m['operation'])
      self.r_operand = m['r_operand']
    self.id = m['id']
    if self.id == 'root':
      self.type = MonkeyType.ROOT
    if self.id == 'humn':
      self.type = MonkeyType.HUMAN

  def value(self, monkeys: Dict[str, Monkey]) -> Union[ValueType, int]:
    if self._value is not None:
      return self._value
    elif self.type == MonkeyType.HUMAN:
      return ValueType.DEPENDENT
    elif self.type == MonkeyType.NUMBER:
      return self.num
    else:
      assert self.type == MonkeyType.OPERATION or self.type == MonkeyType.ROOT
      l_val = monkeys[self.l_operand].value(monkeys)
      r_val = monkeys[self.r_operand].value(monkeys)
      if l_val == ValueType.DEPENDENT or r_val == ValueType.DEPENDENT:
        return ValueType.DEPENDENT
      if self.operation == Operation.ADD:
        self._value = l_val + r_val
      elif self.operation == Operation.MULTIPLY:
        self._value = l_val * r_val
      elif self.operation == Operation.DIVIDE:
        self._value = l_val // r_val
      else:
        assert self.operation == Operation.SUBTRACT
        self._value = l_val - r_val
      return self._value

  def force_value(self, monkeys: Dict[str, Monkey], val: int):
    assert self.type != MonkeyType.NUMBER and self.type != MonkeyType.ROOT
    if self.type == MonkeyType.HUMAN:
      self.num = val
      self._value = val
    else:
      assert self.type == MonkeyType.OPERATION
      l_val = monkeys[self.l_operand].value(monkeys)
      r_val = monkeys[self.r_operand].value(monkeys)
      assert l_val != ValueType.DEPENDENT or r_val != ValueType.DEPENDENT
      if l_val == ValueType.DEPENDENT:
        if self.operation == Operation.ADD:
          monkeys[self.l_operand].force_value(monkeys, val - r_val)
        elif self.operation == Operation.SUBTRACT:
          monkeys[self.l_operand].force_value(monkeys, val + r_val)
        elif self.operation == Operation.MULTIPLY:
          monkeys[self.l_operand].force_value(monkeys, val // r_val)
        elif self.operation == Operation.DIVIDE:
          monkeys[self.l_operand].force_value(monkeys, val * r_val)
      else:
        assert r_val == ValueType.DEPENDENT
        if self.operation == Operation.ADD:
          monkeys[self.r_operand].force_value(monkeys, val - l_val)
        elif self.operation == Operation.SUBTRACT:
          monkeys[self.r_operand].force_value(monkeys, l_val - val)
        elif self.operation == Operation.MULTIPLY:
          monkeys[self.r_operand].force_value(monkeys, val // l_val)
        elif self.operation == Operation.DIVIDE:
          monkeys[self.r_operand].force_value(monkeys, l_val // val)

  def force_equality(self, monkeys: Dict[str, Monkey]):
    assert self.type == MonkeyType.ROOT
    l_val = monkeys[self.l_operand].value(monkeys)
    r_val = monkeys[self.r_operand].value(monkeys)
    assert l_val != ValueType.DEPENDENT or r_val != ValueType.DEPENDENT
    if l_val == ValueType.DEPENDENT:
      monkeys[self.l_operand].force_value(monkeys, r_val)
    else:
      assert r_val == ValueType.DEPENDENT
      monkeys[self.r_operand].force_value(monkeys, l_val)
        
class Solution(SolutionABC):
  def __init__(
    self,
  ):
    self.monkeys: Dict[str, Monkey] = {}

  def parse_row(
    self,
    row: str,
  ):
    self.monkeys[row[:4]] = Monkey(row)

  def solve(
    self,
  ) -> Union[int, str]:
    self.monkeys['root'].force_equality(self.monkeys)
    return self.monkeys['humn'].value(self.monkeys)