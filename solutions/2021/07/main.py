import csv
import statistics
from typing import List

def parse_input(filename: str) -> List[List[int]]:
  positions = []
  with open(filename) as infile:
    input_reader = csv.reader(infile)
    for line in input_reader:
      positions.append(
        [int(position) for position in line]
      )
  return positions

class Crabs:
  def __init__(self, positions: List[int]):
    self._positons = positions

  def optimal_fuel(self):
    min_position = min(positions)
    fuels = [((position - min_position)**2 + (position - min_position)) / 2 for position in positions]
    fuels_change = [
      1 if position == min_position else min_position - position for position in positions
    ]
    while sum(fuels_change) < 0:
      fuels = [fuels[i] + fuels_change[i] for i in range(len(fuels))]
      fuels_change = [fuel_change + (1 if fuel_change != -1 else 2) for fuel_change in fuels_change]
    return sum(fuels)
      

if __name__ == '__main__':
  positions = parse_input('input/input.csv')[0]
  median = round(statistics.median(positions), 0)
  fuels = [abs(position - median) for position in positions]
  print(sum(fuels))
  crabs = Crabs(positions)
  print(crabs.optimal_fuel())