from typing import List

def priority(char: str) -> int:
  if not (len(char) == 1 and char.isalpha()):
    raise Exception('Must be a single alphabetical character')
  elif char.isupper():
    return 27 + ord(char) - ord('A')
  else:
    assert char.islower()
    return 1 + ord(char) - ord('a')

class Rucksack:
  def __init__(self, items: str):
    num_items = len(items)
    self.items = items
    self._compartments = [
      items[:num_items // 2],
      items[num_items // 2:],
    ]

  def item_in_both_compartments(self) -> str:
    set_intersection = set(self._compartments[0]).intersection(set(self._compartments[1]))
    assert len(set_intersection) == 1
    item_in_both = set_intersection.pop()
    assert len(item_in_both) == 1
    return item_in_both

def parse_input(filename: str) -> List[Rucksack]:
  rucksacks = []
  with open(filename) as f:
    for l in f:
      rucksacks.append(Rucksack(l.rstrip()))
  return rucksacks

if __name__ == '__main__':
  rucksacks = parse_input('example_input.txt')
  print(sum(priority(rucksack.item_in_both_compartments()) for rucksack in rucksacks))
  p = 0
  for i in range(0, len(rucksacks), 3):
    group_rucksacks = rucksacks[i : i + 3]
    shared_item_set = set(group_rucksacks[0].items).intersection(
      set(group_rucksacks[1].items),
      set(group_rucksacks[2].items),
    )
    assert len(shared_item_set) == 1
    shared_item = shared_item_set.pop()
    assert len(shared_item) == 1
    p += priority(shared_item)
  print(p)