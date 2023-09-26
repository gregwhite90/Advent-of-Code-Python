import statistics
from collections import deque

OPENING_TO_CLOSING = {
  '(': ')',
  '[': ']',
  '{': '}',
  '<': '>',
}

CLOSING_TO_POINTS = {
  ')': 1,
  ']': 2,
  '}': 3,
  '>': 4,
}

if __name__ == '__main__':
  incomplete_line_points = []
  with open('input/input.txt') as f:
    for line in f:
      corrupted = False
      expected_closings = deque()
      for char in line.rstrip():
        if char in OPENING_TO_CLOSING:
          expected_closings.append(OPENING_TO_CLOSING[char])
        elif expected_closings.pop() != char:
          corrupted = True
          break
      if corrupted: continue
      points = 0
      while len(expected_closings) > 0:
        points = points * 5 + CLOSING_TO_POINTS[expected_closings.pop()]
      incomplete_line_points.append(points)
        
  print(statistics.median(incomplete_line_points))