from collections import defaultdict
from typing import FrozenSet, Set, List

SEGMENTS_TO_DIGIT = {
  frozenset('abcefg'): 0,
  frozenset('cf'): 1,
  frozenset('acdeg'): 2,
  frozenset('acdfg'): 3,
  frozenset('bcdf'): 4,
  frozenset('abdfg'): 5,
  frozenset('abdefg'): 6,
  frozenset('acf'): 7,
  frozenset('abcdefg'): 8,
  frozenset('abcdfg'): 9,
}

class Entry:
  def __init__(self, line: str):
    signal_patterns, output_values = line.split('|')
    self._signal_patterns = signal_patterns.split()
    self._output_values = output_values.split()
    segment_to_wire = {}
    len_to_signal_patterns = defaultdict(list)
    for sp in self._signal_patterns:
      len_to_signal_patterns[len(sp)].append(sp)
    assert len(len_to_signal_patterns[2]) == 1
    assert len(len_to_signal_patterns[3]) == 1
    assert len(len_to_signal_patterns[4]) == 1
    assert len(len_to_signal_patterns[5]) == 3
    assert len(len_to_signal_patterns[6]) == 3
    assert len(len_to_signal_patterns[7]) == 1
    (segment_to_wire['a'], ) = set(len_to_signal_patterns[3][0]) - set(len_to_signal_patterns[2][0])

    four_plus_a = set(len_to_signal_patterns[4][0]).union(set(segment_to_wire['a']))
    for sp in len_to_signal_patterns[6]:
      if four_plus_a.issubset(set(sp)):
        (segment_to_wire['g'], ) = set(sp) - four_plus_a
        break

    (segment_to_wire['e'], ) = set(len_to_signal_patterns[7][0]) - set(len_to_signal_patterns[4][0]) - set(segment_to_wire['a']) - set(segment_to_wire['g'])

    seven_plus_e_plus_g = set(len_to_signal_patterns[3][0]).union(set(segment_to_wire['e']), set(segment_to_wire['g']))
    for sp in len_to_signal_patterns[6]:
      if seven_plus_e_plus_g.issubset(set(sp)):
        (segment_to_wire['b'], ) = set(sp) - seven_plus_e_plus_g
        break

    (segment_to_wire['d'], ) = set(len_to_signal_patterns[4][0]) - set(len_to_signal_patterns[2][0]) - set(segment_to_wire['b'])

    for sp in len_to_signal_patterns[5]:
      if segment_to_wire['e'] in set(sp):
        (segment_to_wire['c'], ) = set(sp) - set(segment_to_wire['e']) - set(segment_to_wire['a']) - set(segment_to_wire['d']) - set(segment_to_wire['g'])
      elif segment_to_wire['b'] in set(sp):
        (segment_to_wire['f'], ) = set(sp) - set(segment_to_wire['b']) - set(segment_to_wire['a']) - set(segment_to_wire['d']) - set(segment_to_wire['g'])
    
    self._wire_to_segment = {
      v: k for k, v in segment_to_wire.items()
    }

  def output_values_of_length(
    self,
    lengths: Set[int] = set([2, 3, 4, 7]),
  ):
    return sum(len(ov) in lengths for ov in self._output_values)

  """
  def _value_to_digit(self, value: str) -> int:
    return self._segments_to_digit[set(value)]
  """

  def _ciphertext_to_segments(self, ciphertext: str) -> FrozenSet[str]:
    return frozenset(self._wire_to_segment[char] for char in ciphertext)

  def _segments_to_digit(self, segments: FrozenSet[str]) -> int:
    return SEGMENTS_TO_DIGIT[segments]

  def output_value_number(self) -> int:
    return int(
      ''.join(
        str(self._segments_to_digit(self._ciphertext_to_segments(ov))) for ov in self._output_values
      )
    )

def parse_input(filename: str) -> List[Entry]:
  entries = []
  with open(filename) as infile:
    for line in infile:
      entries.append(Entry(line))
  return entries

if __name__ == '__main__':
  entries = parse_input('input.txt')
  print(sum(entry.output_values_of_length() for entry in entries))
  print(sum(entry.output_value_number() for entry in entries))