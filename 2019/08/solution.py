from typing import Union, List

from shared import SolutionABC

LAYER_WIDTH = 25
LAYER_HEIGHT = 6

OUTPUT_MAPPING = {
  '0': ' ',
  '1': '#',
}

class Image:
  def __init__(
    self,
  ):
    self.visible_layer: List[str] = None

  def add_layer(
    self,
    digits: List[str],
  ):
    if self.visible_layer is None:
      self.visible_layer = digits
    else:
      assert len(self.visible_layer) == len(digits)
    for i in range(len(digits)):
      if self.visible_layer[i] == '2':
        self.visible_layer[i] = digits[i]

  def __str__(
    self,
  ):
    res = ''
    for y in range(LAYER_HEIGHT):
      res += ''.join(
        [OUTPUT_MAPPING[vl] for vl in
        self.visible_layer[y * LAYER_WIDTH: (y + 1) * LAYER_WIDTH]]
      )
      res += '\n'
    return res

class Solution(SolutionABC):
  def __init__(
    self,
  ):
    self.image = Image()

  def parse_row(
    self,
    row: str,
  ):
    layer_size = LAYER_HEIGHT * LAYER_WIDTH
    assert len(row) % layer_size == 0
    for i in range(len(row) // layer_size):
      self.image.add_layer(
        list(row[i * layer_size : (i + 1) * layer_size])
      )

  def solve(
    self,
  ) -> Union[int, str]:
    return self.image