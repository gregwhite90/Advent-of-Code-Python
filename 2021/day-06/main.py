import csv
from typing import List
from collections import defaultdict

class LanternfishSchool:
  def __init__(
    self,
    timers: List[int],
    incubation: int = 7,
  ):
    self._INCUBATION = incubation
    self._timers = defaultdict(int)
    for timer in timers:
      self._timers[timer] += 1

  def _progress_one_day(self):
    new_timers = defaultdict(int)
    for timer, fish in self._timers.items():
      new_timers[timer - 1] = fish
    birthing_fish = new_timers[-1]
    new_timers[self._INCUBATION - 1] += birthing_fish
    new_timers[self._INCUBATION + 1] += birthing_fish
    new_timers[-1] = 0
    self._timers = new_timers

  def progress_days(self, days: int):
    for _ in range(days):
      self._progress_one_day()

  def num_fish(self):
    return sum(fish for fish in self._timers.values())

def parse_input(filename: str) -> List[LanternfishSchool]:
  lanternfish_schools = []
  with open(filename) as infile:
    input_reader = csv.reader(infile)
    for line in input_reader:
      lanternfish_schools.append(
        LanternfishSchool(
          [
            int(timer) for timer in line
          ]
        )
      )
  return lanternfish_schools

if __name__ == '__main__':
  lanternfish_school = parse_input('input/input.csv')[0]
  lanternfish_school.progress_days(80)
  print(lanternfish_school.num_fish())
  lanternfish_school.progress_days(256-80)
  print(lanternfish_school.num_fish())