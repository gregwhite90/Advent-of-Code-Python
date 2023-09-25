import csv

INPUT_FILENAME = 'input/input.csv'

def part_one():
  with open(INPUT_FILENAME) as input_file:
    input_reader = csv.reader(input_file)
    x = 0
    depth = 0
    for line in input_reader:
      directive = line[0].split(' ')
      direction = directive[0]
      distance = int(directive[1])
      if direction == 'forward': x += distance
      elif direction == 'up': depth -= distance
      elif direction == 'down': depth += distance
    return x * depth

def part_two():
  with open(INPUT_FILENAME) as input_file:
    input_reader = csv.reader(input_file)
    x = 0
    depth = 0
    aim = 0
    for line in input_reader:
      directive = line[0].split(' ')
      direction = directive[0]
      distance = int(directive[1])
      if direction == 'forward':
        x += distance
        depth += aim * distance
      elif direction == 'up': aim -= distance
      elif direction == 'down': aim += distance
    return x * depth

if __name__ == '__main__':
  print(part_one())
  print(part_two())