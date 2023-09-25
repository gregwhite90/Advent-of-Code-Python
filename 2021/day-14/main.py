from collections import defaultdict, namedtuple
from typing import Dict, DefaultDict

Status = namedtuple(
  'Status',
  [
    'polymers',
    'steps',
  ],
)

class Polymerization:
  def __init__(self):
    self._template: str = None
    self._rules: Dict[str, str] = {}
    self._cached_element_counts: Dict[Status, DefaultDict[str, int]] = {}

  def add_template(self, row: str):
    self._template = row

  def add_rule(self, row: str):
    pair, insertion = row.split(' -> ')
    self._rules[pair] = insertion

  def _element_counts(
    self,
    status: Status,
  ) -> DefaultDict[str, int]:
    if status in self._cached_element_counts:
      return self._cached_element_counts[status]
    elif status.steps == 0:
      counts = defaultdict(int)
      for char in status.polymers:
        counts[char] += 1
      self._cached_element_counts[status] = counts
      return counts
    else:
      counts = defaultdict(int)
      for i in range(len(status.polymers) - 1):
        pair = status.polymers[i : i + 2]
        subcount = self._element_counts(
          Status(
            pair[0] + self._rules[pair] + pair[1],
            status.steps -1
          )
        )
        for k, v in subcount.items():
          counts[k] += v
        if i != 0:
          counts[pair[0]] -= 1
      self._cached_element_counts[status] = counts
      return counts

  def counts_after_steps(
    self, 
    steps: int = 10,
  ) -> DefaultDict[str, int]:
    return self._element_counts(Status(self._template, steps))

def max_less_min(
  element_counts: DefaultDict[str, int],
) -> int:
  max = None
  min = None
  for char, count in element_counts.items():
    if not max or count > max:
      max = count
    if not min or count < min:
      min = count
  return max - min

def parse_input(filename: str) -> Polymerization:
  polymerization = Polymerization()
  with open(filename) as f:
    for l in f:
      if len(l.rstrip()) == 0: continue
      elif ' -> ' in l:
        polymerization.add_rule(l.rstrip())
      else:
        polymerization.add_template(l.rstrip())
  return polymerization

if __name__ == '__main__':
  polymerization = parse_input('input.txt')
  print(
    max_less_min(
      polymerization.counts_after_steps(steps = 40)
    )
  )