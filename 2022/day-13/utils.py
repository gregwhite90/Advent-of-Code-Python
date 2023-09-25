import abc
from typing import Union

class SolutionABC(abc.ABC):
  @abc.abstractmethod
  def parse_row(self, row: str):
    pass

  @abc.abstractmethod
  def solve(self) -> Union[int, str]:
    pass

def parse_input(
  soln: SolutionABC,
  filename: str = 'input.txt',
):
  with open(filename) as f:
    for l in f:
      soln.parse_row(l.rstrip('\n'))