from typing import List, NamedTuple, Dict
from enum import Enum

from solutions.shared import SolutionABC, IntcodeComputer, InputMode

class Position(NamedTuple):
  x: int
  y: int

class TileType(Enum):
  EMPTY = 0
  WALL = 1
  BLOCK = 2
  HORIZONTAL_PADDLE = 3
  BALL = 4

TILE_TYPE_TO_STR = {
  TileType.EMPTY: ' ',
  TileType.WALL: 'X',
  TileType.BLOCK: '#',
  TileType.HORIZONTAL_PADDLE: '-',
  TileType.BALL: '*',
}

TILE_DEFINITION_LENGTH = 3

class ArcadeCabinet:
  def __init__(
    self,
    ic: IntcodeComputer,
  ):
    self.ic = ic
    self.tiles: Dict[Position, TileType] = {}
    self.score = 0
    self.min_x = 0
    self.max_x = 0
    self.min_y = 0
    self.max_y = 0
    self.horizontal_paddle: Position = None
    self.ball: Position = None

  def process_output_triple(
    self,
    x: int,
    y: int,
    tile_type: int,
  ):
    if x == -1 and y == 0:
      self.score = tile_type
    else:
      self.max_x = max(x, self.max_x)
      self.max_y = max(y, self.max_y)
      self.min_y = min(y, self.min_y)
      self.min_x = min(x, self.min_x)
      self.tiles[Position(x, y)] = TileType(tile_type)
      if TileType(tile_type) == TileType.HORIZONTAL_PADDLE:
        self.horizontal_paddle = Position(x, y)
      if TileType(tile_type) == TileType.BALL:
        self.ball = Position(x, y)

  def draw_tiles(
    self,
  ):
    self.ic.run()
    outputs = self.ic.get_outputs()
    for i in range(0, len(outputs), TILE_DEFINITION_LENGTH):
      x, y, tile_type = outputs[i : i + TILE_DEFINITION_LENGTH]
      self.process_output_triple(x, y, tile_type)

  def num_block_tiles(
    self,
  ) -> int:
    return sum(
      tile_type == TileType.BLOCK for tile_type in self.tiles.values()
    )

  def enqueue_input(self, input: int):
    self.ic.enqueue_input(input)

  def game_over(
    self,
  ) -> bool:
    return self.ic.is_halted()

  def __str__(self) -> str:
    res = f"Score: {self.score}\n"
    for y in range(self.min_y, self.max_y + 1):
      for x in range(self.min_x, self.max_x + 1):
        res += TILE_TYPE_TO_STR[self.tiles[Position(x, y)]]
      res += '\n'
    return res

class Solution(SolutionABC):
  def __init__(
    self,
  ):
    self.base_program: List[int] = None

  def parse_row(
    self,
    row: str,
  ):
    self.base_program = [int(val) for val in row.split(',')]

  def solve(
    self,
  ) -> int:
    ac = ArcadeCabinet(IntcodeComputer(self.base_program.copy(), [], []))
    ac.draw_tiles()
    while not ac.game_over():
      joystick = 0 if ac.ball.x == ac.horizontal_paddle.x else (
        (ac.ball.x - ac.horizontal_paddle.x) // abs(ac.ball.x - ac.horizontal_paddle.x)
      )
      ac.enqueue_input(joystick)      
      ac.draw_tiles()
      print(ac)
    return ac.score