import abc
from typing import Union, List, Tuple

class SolutionABC(abc.ABC):
  @abc.abstractmethod
  def parse_row(self, row: str):
    pass

  @abc.abstractmethod
  def solve(self) -> Union[int, str, Tuple[int], Tuple[str]]:
    pass

def parse_input(
  soln: SolutionABC,
  path_elements: List[str],
  filename: str = None,
):
  filename = filename or f'solutions/{"/".join(path_elements)}/input/input.txt'
  with open(filename) as f:
    for l in f:
      soln.parse_row(l.rstrip('\n'))

def print_solution(
    soln: SolutionABC,
    path_elements: List[str],
):
  parse_input(soln, path_elements)
  print(soln.solve())