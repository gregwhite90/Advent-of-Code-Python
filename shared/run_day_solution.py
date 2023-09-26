import importlib
import argparse

from shared import print_solution

parser = argparse.ArgumentParser(
  description="Run a solution to a day's Advent of Code",
)
parser.add_argument(
  'year',
  type=int,
  choices=range(2015, 2023),
  metavar='year [2015-2022]',
  help="The year (2015-2022) of the Advent of Code day's solution to run",
)
parser.add_argument(
  'day',
  type=int,
  choices=range(1,26),
  metavar='day [1-25]',
  help="The day (1-25) of the Advent of Code solution to run",
)
parser.add_argument(
  '-p',
  '--part',
  type=str,
  choices={'one', 'two'},
  default='two',
  help="Specify part one or part two. \
    Only applicable for some days. Default is 'two'",
)

def main():
  args = parser.parse_args()
  path_elements = [f'{args.year}', f'{args.day:02}']
  part_sub_module_name = f'part_{args.part}'
  try:
    if importlib.util.find_spec(
      f'{".".join(path_elements)}.{part_sub_module_name}',
    ):
      path_elements += [part_sub_module_name]
    else:
      if args.part == 'one':
        print('Note: this day does not have a separate part one. Part two answer:')
  except ModuleNotFoundError:
    print(f'No solution found for {args.year} day {args.day}.')
  else:
    try:
      solution = importlib.import_module(
        f'{".".join(path_elements)}.solution',
      )
      soln = solution.Solution()
    except ModuleNotFoundError:
      print(f'No solution found for {args.year} day {args.day}.')
    except AttributeError:
      print(f'{args.year} day {args.day} solution is not compatible with shared main script.')
    else:
      print_solution(soln, path_elements)   

if __name__ == '__main__':
  main()