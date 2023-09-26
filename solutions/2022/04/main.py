from __future__ import annotations

class Assignment:
  def __init__(self, assignment_str: str):
    self.start, self.end = (
      int(section) for section in assignment_str.split('-')
    )

  def contains(self, other: Assignment) -> bool:
    return self.start <= other.start and self.end >= other.end

  def overlaps(self, other: Assignment) -> bool:
    return (
      self.end >= other.start
      and self.start <= other.end
    ) or (
      other.end >= self.start
      and other.start <= self.end
    )

if __name__ == '__main__':
  containments = 0
  overlaps = 0
  with open('input/input.txt') as f:
    for l in f:
      assignments = [
        Assignment(assignment_str)
        for assignment_str
        in l.rstrip().split(',')
      ]
      if assignments[0].contains(assignments[1]) or assignments[1].contains(assignments[0]):
        containments += 1
      if assignments[0].overlaps(assignments[1]):
        overlaps += 1
    print(containments)
    print(overlaps)