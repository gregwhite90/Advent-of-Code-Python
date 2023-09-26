import re
from collections import defaultdict, deque
from typing import List, Tuple, DefaultDict, FrozenSet, NamedTuple, Set, Dict

import numpy as np
import numpy.typing as npt

from shared import SolutionABC

class Point(NamedTuple):
  x: int
  y: int
  z: int

class AbsoluteOrienter(NamedTuple):
  transformation_matrix: npt.ArrayLike
  translation_vector: npt.ArrayLike

SCANNER_RE = re.compile(r"\-\-\- scanner (?P<id>\d+) \-\-\-")

class Scanner:
  """A scanner that knows about a list of beacons.

  Scanners know about a list of beacons, relative to their own orientation.
  Scanners do not know (at first) their position or orientation relative to
  any other scanners.

  Attributes:
    beacons: A list of positions of beacons relative to this scanner.
    absolute_beacons: A list of positions of beacons relative to scanner 0.
    absolute_orienter: The transformation to apply to each beacon to yield an absolute_beacon.
    pairwise_dists: A mapping of pairwise distances between beacons.
      Keys are sets of 2-tuples: distance and count of axes with that distance.
      Values are lists of 2-tuples: indices in the beacons list of the pair.
  """
  
  def __init__(
    self,
    id: int,
  ):
    """A scanner does not have any data upon initialization."""
    self.id = id
    self.beacons: List[Point] = []
    self.absolute_beacons: List[Point] = None
    self.absolute_orienter: AbsoluteOrienter = None
    self.pairwise_dists: DefaultDict[FrozenSet[Tuple[int, int]], List[Tuple[int, int]]] = defaultdict(list)

  def add_row(
    self,
    row: str,
  ):
    """Adds a beacon to the scanner.

    Args:
      row: A string representation of a beacon's position.
    """
    self.beacons.append(Point(*[int(pos) for pos in row.split(',')]))

  def calculate_pairwise_dists(
    self,
  ):
    """Calculates the distance between all pairs of beacons."""
    for i in range(len(self.beacons)):
      for j in range(i + 1, len(self.beacons)):
        dists = defaultdict(int)
        for axis in range(len(self.beacons[i])):
          dists[abs(self.beacons[i][axis] - self.beacons[j][axis])] += 1
        self.pairwise_dists[frozenset(dists.items())].append((i, j))

  def set_absolute_orienter(self, ao: AbsoluteOrienter):
    self.absolute_orienter = ao

  def absolutely_orient(self):
    assert self.absolute_orienter is not None
    self.absolute_beacons = []
    for beacon in self.beacons:
      abs_beacon_array = np.dot(self.absolute_orienter.transformation_matrix, beacon) + self.absolute_orienter.translation_vector
      self.absolute_beacons.append(Point(*abs_beacon_array))

class Solution(SolutionABC):
  """Determines the unique list of beacons detected by all scanners.
  
  Maintains a list of scanners, finds the beacons overlapping between scanners,
  and determines the orientation of the scanners relative to each other.

  Attributes:
    scanners: The list of scanners.
  """
  
  def __init__(
    self,
  ):
    """The solution is initialized without any data."""
    self.scanners: List[Scanner] = []
    self.relative_scanner_idxs = set()
    self.recent_absolute_orientations = deque([0])

  def parse_row(
    self,
    row: str,
  ):
    """Parses a row from an input representation.

    Args:
      row: The string from the input to be incorporated.
    """
    if len(row) == 0:
      return
    elif SCANNER_RE.match(row):
      m = SCANNER_RE.match(row)
      id = int(m['id'])
      assert len(self.scanners) == id
      self.scanners.append(Scanner(id))
      if id != 0:
        self.relative_scanner_idxs.add(id)
    else:
      self.scanners[-1].add_row(row)

  def calculate_pairwise_dists(self):
    """Calculates the pairwise distance between beacons for each scanner."""
    for scanner in self.scanners:
      scanner.calculate_pairwise_dists()

  def beacon_overlap(self, i: int, j: int) -> Dict[int, int]:
    """
    Returns the indices of the beacons within each scanner mapped i -> j.
    """
    possible_i_to_j: Dict[int, Set[int]] = {}
    possible_j_to_i: Dict[int, Set[int]] = {}
    for dists in self.scanners[i].pairwise_dists.keys():
      if dists not in self.scanners[j].pairwise_dists:
        continue
      i_indices = set(
        index
        for pair in self.scanners[i].pairwise_dists[dists]
        for index in pair
      )
      j_indices = set(
        index
        for pair in self.scanners[j].pairwise_dists[dists]
        for index in pair
      )
      for i_index in i_indices:        
        if i_index not in possible_i_to_j:
          possible_i_to_j[i_index] = j_indices
        else:
          possible_i_to_j[i_index] = possible_i_to_j[i_index].intersection(j_indices)
      for j_index in j_indices:        
        if j_index not in possible_j_to_i:
          possible_j_to_i[j_index] = i_indices
        else:
          possible_j_to_i[j_index] = possible_j_to_i[j_index].intersection(i_indices)          
    assert len(possible_i_to_j) == len(possible_j_to_i)
    # ensure we've found the unique matching.
    for i, j in possible_i_to_j.items():
      assert len(j) == 1
    return {
      i: j.pop() for i, j in possible_i_to_j.items()
    }

  def absolutely_orient_j(self, i: int, j: int) -> bool:
    """Calculates the absolute orientation of scanner index j.

    Args:
      i: the index of an absolute oriented scanner.
      j: the index of the scanner to be absolutely oriented.

    Returns:
      Whether the absolute orientation succeeded (had enough beacon overlap).
    """
    assert i not in self.relative_scanner_idxs and self.scanners[i].absolute_beacons is not None
    beacon_mapping = self.beacon_overlap(i, j)
    if len(beacon_mapping) < 12:
      return False

    # construct the matrix
    beacon_mapping_tuples = [(b_i, b_j) for b_i, b_j in beacon_mapping.items()]
    matrix = np.zeros((12, 12), dtype=int)
    abs_vector = []
    for pt in range(4):
      # only need 4 points
      b_i, b_j = beacon_mapping_tuples[pt]
      for axis in range(3):
        matrix[pt * 3 + axis][3 * axis : 3 * axis + 3] = self.scanners[j].beacons[b_j]
        matrix[pt * 3 + axis][9 + axis] = 1
      abs_vector += [*self.scanners[i].absolute_beacons[b_i]]

    # calculate and reshape the matrix.
    inv = np.linalg.inv(matrix)
    vec = np.rint(np.dot(inv, abs_vector)).astype(int)
    transformation_matrix = vec[:9].reshape((3, 3))
    translation_vector = vec[9:]
    ao = AbsoluteOrienter(transformation_matrix, translation_vector)

    # update scanner j to absolute orientation
    self.scanners[j].set_absolute_orienter(ao)
    self.scanners[j].absolutely_orient()

    # update tracking for which scanners to absolutely orient next
    self.relative_scanner_idxs.remove(j)
    self.recent_absolute_orientations.append(j)
    return True

  def set_scanner_0_as_absolute(self):
    ao = AbsoluteOrienter(np.identity(3, dtype=int), np.zeros(3, dtype=int))
    self.scanners[0].set_absolute_orienter(ao)
    self.scanners[0].absolutely_orient()

  def manhattan_distance(self, i: int, j: int) -> int:
    """Calculates the manhattan distance between scanner with index i and scanner with index j.
    """
    i_vec = self.scanners[i].absolute_orienter.translation_vector
    j_vec = self.scanners[j].absolute_orienter.translation_vector
    return abs(i_vec[0] - j_vec[0]) + abs(i_vec[1] - j_vec[1]) + abs(i_vec[2] - j_vec[2])

  def max_manhattan_distance(self) -> int:
    max_distance = 0
    for i in range(len(self.scanners)):
      for j in range(i + 1, len(self.scanners)):
        max_distance = max(max_distance, self.manhattan_distance(i, j))
    return max_distance
      
  def solve(
    self,
  ) -> Tuple[int]:
    """
    0. make scanner 0 be absolute.
    1. for any scanner with enough overlap with scanner 0, make that absolute.
    2. continue until all are absolute.
    """
    self.calculate_pairwise_dists()
    self.set_scanner_0_as_absolute()
    while len(self.relative_scanner_idxs) > 0:
      i = self.recent_absolute_orientations.popleft()
      for j in list(self.relative_scanner_idxs):
        self.absolutely_orient_j(i, j)
    all_absolute_beacons = set()
    for scanner in self.scanners:
      for absolute_beacon in scanner.absolute_beacons:
        all_absolute_beacons.add(absolute_beacon)
    return (
      len(all_absolute_beacons),
      self.max_manhattan_distance(),
    )