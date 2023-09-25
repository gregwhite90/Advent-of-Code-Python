from utils import parse_input
from solution import *

if __name__ == '__main__':
  soln = Solution()
  parse_input(soln)
  print(soln.solve())