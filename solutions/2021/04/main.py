import csv
from typing import List, Dict
# board data structure has set of undrawn numbers, dict mapping number to row and column, number of undrawn by row, number of undrawn by column
# draw function removes from undrawn numbers, decrements each undrawn by row and column, and returns if the board is complete
# add_line function takes a string line and interprets it

INPUT_FILENAME = 'input/input.csv'

class Coordinates:
  """
  Coordinates on a Bingo Board.

  Attributes:
    row : int
    col : int
  """
  def __init__(self, row, col):
    self.row = row
    self.col = col

class Board:
  """
  A Bingo board.

  Attributes:
    undrawn_nums : set
      The numbers on the board that have yet to be drawn

    num_to_coords : Dict[int, Coordinates]
      The mapping from each number to the Coordinates on the Board

    num_undrawn_by_row : List[int]
      The count of undrawn numbers for each row

    num_undrawn_by_col : List[int]
      The count of undrawn numbers for each column
  """
  
  def __init__(self, dimens: int):
    """
    Inits Board with dimensions dimens x dimens.
    """
    self.undrawn_nums = set()
    self.num_to_coords = {}
    self.num_undrawn_by_row = [dimens] * dimens
    self.num_undrawn_by_col = [dimens] * dimens

  def add_row(self, nums: List[int], row: int):
    """
    Adds a row of numbers to the Board.

    Args:
      nums: The list of numbers in the row.
      row: The index of the row.
    """
    for col, num in enumerate(nums):
      self.undrawn_nums.add(num)
      self.num_to_coords[num] = Coordinates(row, col)

  def draw(self, num: int) -> bool:
    """
    Reflects a number being drawn.

    Args:
      num: The number being drawn.

    Returns:
      Whether the Board is completed after drawing the number.
    """    
    completed = False
    if num in self.undrawn_nums:
      self.undrawn_nums.remove(num)
      coords = self.num_to_coords[num]
      self.num_undrawn_by_row[coords.row] -= 1
      self.num_undrawn_by_col[coords.col] -= 1
      if (
        self.num_undrawn_by_row[coords.row] == 0 or
        self.num_undrawn_by_col[coords.col] == 0
      ):
        completed = True
    return completed

  def undrawn_nums_sum(self) -> int:
    """
    The sum of all undrawn numbers.
    """
    return sum(self.undrawn_nums)

class BingoSetup:
  """
  A setup of Bingo boards and numbers to draw.

  Attributes:
    nums : List[int]
      The numbers to be drawn.
      
    boards : List[Board]
      The Bingo boards.
  """
  
  def __init__(self, infile: str):
    """
    Inits from csv file with filename infile

    Args:
      infile: The filename of the csv file with the setup.
    """
    self.boards = []
    with open(infile) as input_file:
      input_reader = csv.reader(input_file)
      row = 0
      for line_num, line in enumerate(input_reader):
        if line_num == 0:
          self.nums = [int(num) for num in line]
        elif len(line) == 0:
          row = 0
          self.boards.append(Board(5))
        else:
          row_nums = [int(num) for num in line[0].split()]
          self.boards[-1].add_row(row_nums, row)
          row += 1

  def score_of_first(self) -> int:
    """
    The score of the first winning Bingo board.

    Returns:
      The score of the first board to win.         
    """
    for num in self.nums:
      for board in self.boards:
        if board.draw(num):
          return num * board.undrawn_nums_sum()

  def score_of_last(self) -> int:
    """
    The score of the last winning Bingo board.

    Returns:
      The score of the last board to win.         
    """
    scores = []
    for num in self.nums:
      winning_indices = []
      for idx, board in enumerate(self.boards):
        if board.draw(num):
          scores.append(num * board.undrawn_nums_sum())
          winning_indices.append(idx)
      for idx in reversed(winning_indices):
        del self.boards[idx]
      if len(self.boards) == 0: break
    return scores[-1]

def score_of_first(infile: str) -> int:
  """
  The score of the first winning Bingo board.

  Args:
    infile: The filename of the input.

  Returns:
    The score of the first Bingo board to win.
  """
  setup = BingoSetup(infile)
  return setup.score_of_first()

def score_of_last(infile: str) -> int:
  """
  The score of the last winning Bingo board.

  Args:
    infile: The filename of the input.

  Returns:
    The score of the last Bingo board to win.  
  """
  setup = BingoSetup(infile)
  return setup.score_of_last()
    
if __name__ == '__main__':
  print(score_of_first(INPUT_FILENAME))
  print(score_of_last(INPUT_FILENAME))