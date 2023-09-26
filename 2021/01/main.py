import csv
import collections

def line_to_num(line):
  return int(line[0])

def sliding_window_increases(window_size):
  with open('input/input.csv') as input_file:
    input_reader = csv.reader(input_file)
    cur_deque = collections.deque(maxlen=window_size + 1)
    num_increases = 0
    for line in input_reader:
      depth = line_to_num(line)
      cur_deque.append(depth)
      if len(cur_deque) != window_size + 1: continue
      if cur_deque[-1] > cur_deque[0]: num_increases += 1
    return num_increases

if __name__ == '__main__':
  print(sliding_window_increases(1))
  print(sliding_window_increases(3))