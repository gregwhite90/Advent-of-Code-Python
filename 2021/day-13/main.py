import re
from collections import namedtuple

fold_re = re.compile(
  r"fold along (?P<axis>x|y)=(?P<value>\d+)"
)
dot_re = re.compile(
  r"(?P<x>\d+),(?P<y>\d+)"
)

Point = namedtuple(
  'Point',
  [
    'x',
    'y',
  ],
)

class TransparentPaper:
  def __init__(self):
    self._dots = set()
    self._cols = 0
    self._rows = 0

  def add_dot(self, dot_str: str):
    x, y = (
      int(coord) for coord in dot_str.split(',')
    )
    self._dots.add(
      Point(x, y)
    )
    self._cols = max(self._cols, x + 1)
    self._rows = max(self._rows, y + 1)

  def fold(self, fold_str: str):
    m = fold_re.match(fold_str)
    value = int(m['value'])
    new_dots = set()
    for dot in self._dots:
      if m['axis'] == 'y':
        assert dot.y != value
        self._rows = value
        if dot.y < value:
          new_dots.add(dot)
        else:
          new_dots.add(Point(
            dot.x, 2 * value - dot.y
          ))
      else:
        assert m['axis'] == 'x'
        assert dot.x != value
        self._cols = value
        if dot.x < value:
          new_dots.add(dot)
        else:
          new_dots.add(Point(
            2 * value - dot.x, dot.y
          ))
    self._dots = new_dots
    
  def num_dots(self) -> int:
    return len(self._dots)

  def __str__(self) -> str:
    result = "\n"
    for y in range(self._rows):
      for x in range(self._cols):
        if Point(x, y) in self._dots:
          result += "#"
        else:
          result += "."
      result += "\n"
    return result

def parse_input(filename: str, folds: int = None) -> TransparentPaper:
  folds_made = 0
  paper = TransparentPaper()
  with open(filename) as f:
    for l in f:
      if len(l.rstrip()) == 0: continue
      elif fold_re.match(l.rstrip()):
        paper.fold(l.rstrip()) 
        folds_made += 1
      else:
        assert dot_re.match(l.rstrip())
        paper.add_dot(l.rstrip())
      if folds != None and folds_made == folds:
        break
  return paper

if __name__ == '__main__':
  paper = parse_input('input/input.txt')
  print(paper)