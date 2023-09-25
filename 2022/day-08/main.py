from typing import List

MAX_HEIGHT = 9

class Grid:
  def __init__(self):
    self._heights: List[List[int]] = []
    self._visibility_requirements: List[List[int]] = None
    self._scenic_scores: List[List[int]] = None

  def add_row(self, row: str):
    self._heights.append([int(ht) for ht in row])

  def visibility_requirements(self) -> List[List[int]]:
    if not self._visibility_requirements:
      rows = len(self._heights)
      cols = len(self._heights[0])
      max_horizontal_heights = [[0 for _ in range(cols)] for _ in range(rows)]
      for row in range(rows):
        max_left_heights = [-1]
        for col in range(1, cols):
          max_left_heights = max_left_heights + [max(max_left_heights[-1], self._heights[row][col - 1])]
        max_right_heights = [-1]      
        for col in range(cols - 2, -1, -1):
          max_right_heights = [max(max_right_heights[0], self._heights[row][col + 1])] + max_right_heights
        for col in range(cols):
          max_horizontal_heights[row][col] = min(max_left_heights[col], max_right_heights[col])
      self._visibility_requirements = [[0 for _ in range(cols)] for _ in range(rows)]
      for col in range(cols):
        max_up_heights = [-1]
        for row in range(1, rows):
          max_up_heights = max_up_heights + [max(max_up_heights[-1], self._heights[row - 1][col])]
        max_down_heights = [-1]
        for row in range(cols - 2, -1, -1):
          max_down_heights = [max(max_down_heights[0], self._heights[row + 1][col])] + max_down_heights
        for row in range(rows):
          self._visibility_requirements[row][col] = min(
            max_up_heights[row], 
            max_down_heights[row],
            max_horizontal_heights[row][col],
          )
    return self._visibility_requirements

  def scenic_scores(self) -> List[List[int]]:
    if not self._scenic_scores:
      rows = len(self._heights)
      cols = len(self._heights[0])
      self._scenic_scores = [[1 for _ in range(cols)] for _ in range(rows)]
      for row in range(rows):
        left_indices = {
          height: 0 for height in range(MAX_HEIGHT + 1)
        }
        for col in range(cols):
          self._scenic_scores[row][col] *= col - left_indices[self._heights[row][col]]
          for height in range(self._heights[row][col] + 1):
            left_indices[height] = col
        right_indices = {
          height: cols - 1 for height in range(MAX_HEIGHT + 1)
        }
        for col in range(cols - 1, -1, -1):
          self._scenic_scores[row][col] *= right_indices[self._heights[row][col]] - col
          for height in range(self._heights[row][col] + 1):
            right_indices[height] = col
      for col in range(cols):
        up_indices = {
          height: 0 for height in range(MAX_HEIGHT + 1)
        }
        for row in range(rows):
          self._scenic_scores[row][col] *= row - up_indices[self._heights[row][col]]
          for height in range(self._heights[row][col] + 1):
            up_indices[height] = row
        down_indices = {
          height: rows - 1 for height in range(MAX_HEIGHT + 1)
        }
        for row in range(rows - 1, -1, -1):
          self._scenic_scores[row][col] *= down_indices[self._heights[row][col]] - row
          for height in range(self._heights[row][col] + 1):
            down_indices[height] = row
    return self._scenic_scores

  def number_visible(self) -> int:
    return sum(
      self._heights[row][col] > self.visibility_requirements()[row][col]
      for row in range(len(self._heights)) for col in range(len(self._heights[0]))
    )

  def max_scenic_score(self) -> int:
    return max(
      max(self.scenic_scores()[row]) for row in range(len(self._heights))
    )

def parse_input(filename: str) -> Grid:
  grid = Grid()
  with open(filename) as f:
    for l in f:
      grid.add_row(l.rstrip())
  return grid

if __name__ == '__main__':
  grid = parse_input('input.txt')
  print(grid.number_visible())
  print(grid.max_scenic_score())