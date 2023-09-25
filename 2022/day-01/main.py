import csv
from typing import List

class Elf:
  def __init__(self):
    self._calories = []

  def add_calories(self, calories):
    self._calories.append(calories)

  def total_calories(self):
    return sum(self._calories)

def parse_input(filename: str) -> List[Elf]:
  elves = [Elf()]
  with open(filename) as infile:
    input_reader = csv.reader(infile)
    for line_num, line in enumerate(input_reader):
      if len(line) == 0:
        elves.append(Elf())
      else:
        elves[-1].add_calories(int(line[0]))
  return elves

def max_calories(elves: List[Elf]):
  return max([elf.total_calories() for elf in elves])

def top_calories(elves: List[Elf], num: int = 3):
  # mutates the elves argument passed in
  elves.sort(
    key = lambda elf: elf.total_calories(),
    reverse = True,
  )
  return sum([elf.total_calories() for elf in elves[:num]])

if __name__ == '__main__':
  elves = parse_input('input.csv')
  print(max_calories(elves))
  print(top_calories(elves))