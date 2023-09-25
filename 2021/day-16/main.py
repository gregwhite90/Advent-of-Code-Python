from __future__ import annotations
import math
from enum import Enum
from typing import List

VERSION_BITS = 3
TYPE_ID_BITS = 3
LITERAL_VALUE_CHUNK_LEN = 5
OPER_LENGTH_TYPE_ID_0_BITS = 15
OPER_LENGTH_TYPE_ID_1_BITS = 11

def hex_to_bits(hex: str) -> str:
  bits = ''
  for char in hex:
    bits += format(int(char, 16), '04b')
  return bits

class PacketType(Enum):
  OPERATOR = 0
  LITERAL_VALUE = 4

class OperatorPacketType(Enum):
  SUM = 0
  PRODUCT = 1
  MINIMUM = 2
  MAXIMUM = 3
  GREATER_THAN = 5
  LESS_THAN = 6
  EQUAL_TO = 7

class Packet:
  def __init__(self, bits: str):
    self.version = int(bits[ : VERSION_BITS], 2) 
    self.type_id = int(bits[VERSION_BITS : VERSION_BITS + TYPE_ID_BITS], 2)
    self.type = PacketType.LITERAL_VALUE if self.type_id == 4 else PacketType.OPERATOR
    if self.type == PacketType.OPERATOR:
      self.operator_type = OperatorPacketType(self.type_id)
    self.length = VERSION_BITS + TYPE_ID_BITS
    self._children: List[Packet] = []
    if self.type == PacketType.LITERAL_VALUE:
      self._parse_literal_value(bits[self.length : ])
    elif self.type == PacketType.OPERATOR:
      self._parse_operator(bits[self.length : ])

  def _parse_literal_value(self, bits: str):
    idx = 0
    value_str = ''
    while True:
      last_group = bits[idx] == '0'
      value_str += bits[idx + 1 : idx + LITERAL_VALUE_CHUNK_LEN]
      idx += LITERAL_VALUE_CHUNK_LEN
      if last_group: break
    self._value = int(value_str, 2)
    self.length += idx

  def _parse_operator(self, bits: str):
    length_type_id = bits[0]
    self.length += 1
    if length_type_id == '0':
      self._parse_operator_length_type_id_0(bits[1 : ])
    else:
      self._parse_operator_length_type_id_1(bits[1 : ])
    self._parse_operator_value()

  def _parse_operator_length_type_id_0(self, bits: str):
    total_children_length = int(bits[ : OPER_LENGTH_TYPE_ID_0_BITS], 2)
    idx = OPER_LENGTH_TYPE_ID_0_BITS
    while sum(child.length for child in self._children) < total_children_length:
      packet = Packet(bits[idx :])
      self._children.append(packet)
      idx += packet.length
    assert sum(child.length for child in self._children) == total_children_length
    self.length += idx

  def _parse_operator_length_type_id_1(self, bits: str):
    num_children = int(bits[ : OPER_LENGTH_TYPE_ID_1_BITS], 2)
    idx = OPER_LENGTH_TYPE_ID_1_BITS
    for _ in range(num_children):
      packet = Packet(bits[idx : ])
      self._children.append(packet)
      idx += packet.length
    self.length += idx

  def _parse_operator_value(self):
    if self.operator_type == OperatorPacketType.SUM:
      self._parse_sum_value()
    elif self.operator_type == OperatorPacketType.PRODUCT:
      self._parse_product_value()
    elif self.operator_type == OperatorPacketType.MINIMUM:
      self._parse_minimum_value()
    elif self.operator_type == OperatorPacketType.MAXIMUM:
      self._parse_maximum_value()
    elif self.operator_type == OperatorPacketType.GREATER_THAN:
      self._parse_greater_than_value()
    elif self.operator_type == OperatorPacketType.LESS_THAN:
      self._parse_less_than_value()
    elif self.operator_type == OperatorPacketType.EQUAL_TO:
      self._parse_equal_to_value()

  def _parse_sum_value(self):
    self._value = sum(child.value() for child in self._children)

  def _parse_product_value(self):
    self._value = math.prod(child.value() for child in self._children)

  def _parse_minimum_value(self):
    self._value = min(child.value() for child in self._children)

  def _parse_maximum_value(self):
    self._value = max(child.value() for child in self._children)

  def _parse_greater_than_value(self):
    assert len(self._children) == 2
    self._value = 1 if self._children[0].value() > self._children[1].value() else 0

  def _parse_less_than_value(self):
    assert len(self._children) == 2
    self._value = 1 if self._children[0].value() < self._children[1].value() else 0

  def _parse_equal_to_value(self):
    assert len(self._children) == 2
    self._value = 1 if self._children[0].value() == self._children[1].value() else 0

  def value(self) -> int:
    return self._value

  def sum_versions_incl_children(self) -> int:
    return self.version + sum(
      child.sum_versions_incl_children()
      for child in self._children
    )

def parse_input(filename: str) -> List[Packet]:
  packets = []
  with open(filename) as f:
    for l in f:
      packets.append(Packet(hex_to_bits(l.rstrip())))
  return packets

if __name__ == '__main__':
  packets = parse_input('input.txt')
  assert len(packets) == 1
  print(packets[0].sum_versions_incl_children())
  print(packets[0].value())