import re
from typing import NamedTuple, Set

from shared import SolutionABC

DIRECTION_RE = re.compile(r'(ne|se|nw|sw|e|w)')

class Tile(NamedTuple):
  """
  A tile is uniquely defined by these 2-coordinates relative to the reference tile.

  Each direct east / west move is 2 in the coordinate plane, each diagonal move is 1 in
  two directions.
  """
  net_n: int
  net_e: int

def neighbors(tile: Tile) -> Set[Tile]:
  return {
    Tile(tile.net_n + 1, tile.net_e + 1),
    Tile(tile.net_n, tile.net_e + 2),
    Tile(tile.net_n - 1, tile.net_e + 1),
    Tile(tile.net_n + 1, tile.net_e - 1),
    Tile(tile.net_n, tile.net_e - 2),
    Tile(tile.net_n - 1, tile.net_e - 1),
  }

def all_adj_incl_tile(tile: Tile) -> Set[Tile]:
  return neighbors(tile) | {tile}

class Solution(SolutionABC):
  def __init__(
    self,
  ):
    self.black_tiles: Set[Tile] = set()

  def parse_row(
    self,
    row: str,
  ):
    net_n = 0
    net_e = 0
    for dir in re.findall(DIRECTION_RE, row):
      if dir == 'e':
        net_e += 2
      elif dir == 'w':
        net_e -= 2
      elif dir == 'ne':
        net_n += 1
        net_e += 1
      elif dir == 'sw':
        net_n -= 1
        net_e -= 1
      elif dir == 'se':
        net_n -= 1
        net_e += 1
      else:
        assert dir == 'nw'
        net_n += 1
        net_e -= 1
    tile = Tile(net_n, net_e)
    if tile in self.black_tiles:
      self.black_tiles.remove(tile)
    else:
      self.black_tiles.add(tile)

  def progress_day(self):
    considered: Set[Tile] = set()
    new_black_tiles = set()
    for black_tile in self.black_tiles:
      for tile_to_consider in all_adj_incl_tile(black_tile):
        if tile_to_consider in considered:
          continue
        adj_black = sum(adj in self.black_tiles for adj in neighbors(tile_to_consider))
        if (
          tile_to_consider in self.black_tiles and (adj_black == 1 or adj_black == 2)
        ) or (
          tile_to_consider not in self.black_tiles and adj_black == 2
        ):
          new_black_tiles.add(tile_to_consider)
        considered.add(tile_to_consider)

    self.black_tiles = new_black_tiles

  def solve(
    self,
  ) -> int:
    for _ in range(100):
      self.progress_day()
    return len(self.black_tiles)