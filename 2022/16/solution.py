from __future__ import annotations

import re
import heapq
from typing import List, Set, Dict, Deque, NamedTuple
from collections import deque
import itertools

from shared import SolutionABC

counter = itertools.count()

ROW_RE = re.compile(r"Valve (?P<id>\w+) has flow rate=(?P<flow>\d+); tunnels? leads? to valves? (?P<tunnels>[\w \,]+)")
MINUTES = 26

class Progress(NamedTuple):
  """
  Used to calculate the matrix of distances between nonzero-flow valves.
  """
  dist: int
  valve_id: str

class Plan(NamedTuple):
  """
  The current plan of a single actor: which valve they're going to open,
  how long until it's open, and how much guaranteed flow that represents once the plan is executed.
  """
  minutes_remaining: int
  valve_id: str
  uncounted_guarantee: int

class Valve:
  def __init__(
    self,
    id: str,
    flow: int,
    tunnels: List[str],
  ):
    self.id = id
    self.flow = flow
    self.tunnels = tunnels

class Path:
  """
  The current apporach of all actors.
  """
  def __init__(
    self,
    solution: Solution,
    minutes: int,
    plans: List[Plan],
    guaranteed: int,
    unopened: Set[str],
  ):
    self.solution = solution
    self.minutes = minutes
    self.plans = plans
    self.guaranteed = guaranteed
    self.unopened = unopened
    potential_minutes_when_opened = []
    for i in range(1, 2 * len(self.unopened) + 1):
      potential_minutes_when_opened.append(self.minutes - self.plans[0].minutes_remaining - 2 * i)
      potential_minutes_when_opened.append(self.minutes - self.plans[1].minutes_remaining - 2 * i)
    potential_minutes_when_opened.sort(reverse=True)
    shared_len = min(len([p for p in potential_minutes_when_opened if p > 0]), len(self.unopened))
    sorted_flows = [solution.valves[v_id].flow for v_id in self.unopened]
    sorted_flows.sort(reverse=True)
    # take the max sum
    self.potential = sum(
      sorted_flows[i] * potential_minutes_when_opened[i] for i in range(shared_len)
    )
    self.counter = next(counter)

  def __lt__(self, other: Path) -> bool:
    if self.guaranteed + self.potential != other.guaranteed + other.potential:
      return self.guaranteed + self.potential > other.guaranteed + other.potential
    elif self.guaranteed != other.guaranteed:
      return self.guaranteed > other.guaranteed
    else:
      return self.counter < other.counter

class Solution(SolutionABC):
  def __init__(
    self,
  ):
    self.valves: Dict[str, Valve] = {}
    self.distances: Dict[str, Dict[str, int]] = {
      'AA': {}
    }

  def parse_row(
    self,
    row: str,
  ):
    m = ROW_RE.match(row)
    assert m
    id = m['id']
    flow = int(m['flow'])
    self.valves[id] = Valve(
      id,
      flow,
      m['tunnels'].split(', '),
    )
    if flow > 0:
      self.distances[id] = {}

  def _calculate_distances(self):
    nonzero_valve_ids = self._nonzero_valve_ids()
    for orig_pos in ['AA', *nonzero_valve_ids]:
      queue: Deque[Progress] = deque([Progress(0, orig_pos)])
      while len(self.distances[orig_pos]) < len(nonzero_valve_ids):
        progress = queue.popleft()
        if progress.valve_id in nonzero_valve_ids and progress.valve_id not in self.distances[orig_pos]:
          self.distances[orig_pos][progress.valve_id] = progress.dist
          if orig_pos != 'AA':
            self.distances[progress.valve_id][orig_pos] = progress.dist
        for v_id in self.valves[progress.valve_id].tunnels:
          queue.append(Progress(progress.dist + 1, v_id))
    self.distances['AA']['AA'] = 0

  def _options(
    self, 
    path: Path,
  ) -> List[Path]:
    """
    The list of Paths explorable from the current Path.
    """
    # The plans each actor could explore next.
    plans: List[List[Plan]] = []
    for plan in path.plans:
      if plan.minutes_remaining > 0:
        plans.append([plan])
      else:
        # always an option to just wait for other actors to finish.
        plan_options = [Plan(path.minutes, plan.valve_id, 0)]
        for v_id in path.unopened:
          dist = self.distances[plan.valve_id][v_id]
          minutes_remaining = path.minutes - dist - 1
          if minutes_remaining > 0:
            plan_options.append(Plan(
              dist + 1,
              v_id,
              minutes_remaining * self.valves[v_id].flow,
            ))
        plans.append(plan_options)
    path_options = []
    # Tuple unpacking here assumes there are 2 actors
    for plan_0, plan_1 in itertools.product(*plans):
      if plan_0.valve_id != plan_1.valve_id:
        if path.minutes == MINUTES and plan_0.valve_id > plan_1.valve_id:
          continue
        if len(plans[0]) > 1 and len(plans[1]) > 1 and self._dominated(path, plan_0, plan_1):
          # generating a new plan for both at the same time,
          # can rule out dominated if there are strictly dominant options
          continue
        minutes = min(plan_0.minutes_remaining, plan_1.minutes_remaining)
        path_options.append(Path(
          path.solution,
          path.minutes - minutes,
          [
            Plan(plan_0.minutes_remaining - minutes, plan_0.valve_id, 0),
            Plan(plan_1.minutes_remaining - minutes, plan_1.valve_id, 0),
          ],
          path.guaranteed + plan_0.uncounted_guarantee + plan_1.uncounted_guarantee,
          path.unopened - {plan_0.valve_id} - {plan_1.valve_id},
        ))
    return path_options

  def _dominated(self, path: Path, plan_0: Plan, plan_1: Plan) -> bool:
    """
    Returns whether a given pair of plans is fully dominated by the other orientation of it.
    """
    valve_0 = path.plans[0].valve_id
    valve_1 = path.plans[1].valve_id
    return self.distances[valve_0][plan_0.valve_id] > self.distances[valve_1][plan_0.valve_id] and self.distances[valve_1][plan_1.valve_id] > self.distances[valve_0][plan_1.valve_id]

  def _nonzero_valve_ids(self) -> Set[str]:
    return set(id for id, valve in self.valves.items() if valve.flow > 0)

  def _optimal_path(self) -> Path:
    pq: List[Path] = [Path(
      self,
      MINUTES,
      [
        Plan(0, 'AA', 0),
        Plan(0, 'AA', 0),
      ],
      0,
      self._nonzero_valve_ids(),
    )]
    while True:
      path = heapq.heappop(pq)
      if path.minutes == 0 or len(path.unopened) == 0:
        return path
      else:
        options = self._options(path)
        for option in options:
          heapq.heappush(pq, option)

  def solve(
    self,
  ) -> int:
    self._calculate_distances()
    path = self._optimal_path()
    return path.guaranteed