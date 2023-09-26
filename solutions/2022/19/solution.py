from __future__ import annotations
import re
import heapq
import itertools
import math
from collections import defaultdict
from typing import NamedTuple, List, DefaultDict, Set, Dict

from solutions.shared import SolutionABC

TIME = 32
BLUEPRINTS = 3
MAX_RESOURCE_REQUIREMENT = 20

class ResourceSufficiencyStatus(NamedTuple):
  minutes_left: int
  robots: int
  cost: int

def resources_to_build_to_end(rss: ResourceSufficiencyStatus) -> int:
  return max(rss.cost, rss.cost + (rss.cost - rss.robots) * (rss.minutes_left - 2))

class TimeToResourceStatus(NamedTuple):
  required: int
  capacity: int
  time_to_predecessor: int

TIME_TO_RESOURCES: Dict[TimeToResourceStatus, int] = {}
for required in range(1, MAX_RESOURCE_REQUIREMENT + 1):
  for capacity in range(TIME + 1):
    for next_pred_minutes in range(TIME + 1):
      mins = 0
      pred = 0
      while mins < TIME and pred < required:    
        mins += 1
        pred += capacity + max(0, mins - next_pred_minutes)
      TIME_TO_RESOURCES[TimeToResourceStatus(required, capacity, next_pred_minutes)] = mins


BLUEPRINT_RE = re.compile(r"Blueprint (?P<id>\d+): Each ore robot costs (?P<ore_cost>\d+) ore\. Each clay robot costs (?P<clay_cost>\d+) ore\. Each obsidian robot costs (?P<obsidian_ore_cost>\d+) ore and (?P<obsidian_clay_cost>\d+) clay\. Each geode robot costs (?P<geode_ore_cost>\d+) ore and (?P<geode_obsidian_cost>\d+) obsidian\.")

counter = itertools.count()

class ResourceClasses(NamedTuple):
  ore: int
  clay: int
  obsidian: int

class FactoryStatus(NamedTuple):
  robots: ResourceClasses
  minutes: int

class ResourceStatus(NamedTuple):
  resources: ResourceClasses
  guaranteed: int

def enough(resources: ResourceClasses, cost: ResourceClasses) -> bool:
  for i in range(len(resources)):
    if resources[i] < -cost[i]:
      return False
  return True

class Blueprint:
  def __init__(self, row: str):
    m = BLUEPRINT_RE.match(row)
    assert m
    self.id = int(m['id'])
    self.ore_cost = ResourceClasses(-int(m['ore_cost']), 0, 0)
    self.clay_cost = ResourceClasses(-int(m['clay_cost']), 0, 0)
    self.obsidian_cost = ResourceClasses(
      -int(m['obsidian_ore_cost']), 
      -int(m['obsidian_clay_cost']), 
      0,
    )
    self.geode_cost = ResourceClasses(
      -int(m['geode_ore_cost']), 
      0,
      -int(m['geode_obsidian_cost']),
    )
    self._most_geodes = None
    
  def most_geodes(self) -> int:
    if self._most_geodes is not None:
      return self._most_geodes

    most_possible_resources: DefaultDict[FactoryStatus, Set[ResourceStatus]] = defaultdict(set)
    
    pq = [Plan(
      self,
      ResourceClasses(1, 0, 0),
      ResourceClasses(0, 0, 0),
      0,
      TIME,
    )]
    
    while True:
      plan = heapq.heappop(pq)
      if plan.minutes == 0 or plan.potential == 0:
        self._most_geodes = plan.guaranteed
        return self._most_geodes
      if plan.resources.ore >= resources_to_build_to_end(
        ResourceSufficiencyStatus(
          plan.minutes,
          plan.robots.ore,
          - self.geode_cost.ore,
        )
      ) and plan.resources.obsidian >= resources_to_build_to_end(
        ResourceSufficiencyStatus(
          plan.minutes,
          plan.robots.obsidian,
          - self.geode_cost.obsidian,
        )
      ):
        self._most_geodes = plan.guaranteed + plan.potential
        return self._most_geodes
      mprs = most_possible_resources[FactoryStatus(plan.robots, plan.minutes)]
      if plan.is_dominated(mprs):
        rs = ResourceStatus(plan.resources, plan.guaranteed)
        if rs in mprs:
          mprs.remove(rs)
        continue
      for option in plan.options():
        mprs = most_possible_resources[FactoryStatus(option.robots, option.minutes)]
        if not option.is_dominated(mprs):
          mprs.add(ResourceStatus(option.resources, option.guaranteed))
          heapq.heappush(pq, option)

class Plan:
  def __init__(
    self,
    blueprint: Blueprint,
    robots: ResourceClasses,
    resources: ResourceClasses,
    guaranteed: int,
    minutes: int,
  ):
    self.blueprint = blueprint
    self.robots = robots
    self.resources = resources
    self.guaranteed = guaranteed
    self.minutes = minutes
    # assumes building one geode-cracking robot each minute, starting from the first buildable geode robot
    # potential only strictly required to be an upper bound, the trade-off is speed to calculate vs.
    # tightness to the actual potential (in particular, want to identify low and zero potential states)
    next_geode_minutes = self._next_geode_minutes()
    self.potential = max((minutes - next_geode_minutes) * (minutes - next_geode_minutes - 1) // 2, 0)
    self.counter = next(counter)

  def _next_clay_minutes(self) -> int:
    # assumes can build more ore robots immediately and indefinitely
    if self.resources.ore >= - self.blueprint.clay_cost.ore:
      return 0
    else:
      return TIME_TO_RESOURCES[TimeToResourceStatus(
        -self.blueprint.clay_cost.ore - self.resources.ore,
        self.robots.ore,
        0,
      )]

  def _next_obsidian_minutes(self) -> int:
    # assumes ore is not a limiting resource
    if self.resources.clay >= - self.blueprint.obsidian_cost.clay:
      return 0
    else:
      return TIME_TO_RESOURCES[TimeToResourceStatus(
        -self.blueprint.obsidian_cost.clay - self.resources.clay,
        self.robots.clay,
        self._next_clay_minutes(),
      )]

  def _next_geode_minutes(self) -> int:
    # assumes ore is not a limiting resource
    if self.resources.obsidian >= - self.blueprint.geode_cost.obsidian:
      return 0
    else:
      return TIME_TO_RESOURCES[TimeToResourceStatus(
        -self.blueprint.geode_cost.obsidian - self.resources.obsidian,
        self.robots.obsidian,
        self._next_obsidian_minutes(),
      )]

  def options(self) -> List[Plan]:
    new_resources = ResourceClasses(*[sum(r) for r in zip(self.resources, self.robots)])
    options = [Plan(
        self.blueprint,
        self.robots,
        new_resources,
        self.guaranteed,
        self.minutes - 1,
      )]
    if enough(self.resources, self.blueprint.ore_cost):
      options.append(Plan(
        self.blueprint,
        ResourceClasses(*[sum(r) for r in zip(self.robots, ResourceClasses(1, 0, 0))]),
        ResourceClasses(*[sum(r) for r in zip(new_resources, self.blueprint.ore_cost)]),
        self.guaranteed,
        self.minutes - 1,
      ))
    if enough(self.resources, self.blueprint.clay_cost):
      options.append(Plan(
        self.blueprint,
        ResourceClasses(*[sum(r) for r in zip(self.robots, ResourceClasses(0, 1, 0))]),
        ResourceClasses(*[sum(r) for r in zip(new_resources, self.blueprint.clay_cost)]),
        self.guaranteed,
        self.minutes - 1,
      ))
    if enough(self.resources, self.blueprint.obsidian_cost):
      options.append(Plan(
        self.blueprint,
        ResourceClasses(*[sum(r) for r in zip(self.robots, ResourceClasses(0, 0, 1))]),
        ResourceClasses(*[sum(r) for r in zip(new_resources, self.blueprint.obsidian_cost)]),
        self.guaranteed,
        self.minutes - 1,
      ))
    if enough(self.resources, self.blueprint.geode_cost):
      options.append(Plan(
        self.blueprint,
        self.robots,
        ResourceClasses(*[sum(r) for r in zip(new_resources, self.blueprint.geode_cost)]),
        self.guaranteed + (self.minutes - 1),
        self.minutes - 1,
      ))
    return options

  def __lt__(self, other: Plan) -> bool:
    if self.guaranteed + self.potential != other.guaranteed + other.potential:
      return self.guaranteed + self.potential > other.guaranteed + other.potential
    elif self.guaranteed != other.guaranteed:
      return self.guaranteed > other.guaranteed
    elif self.minutes != other.minutes:
      return self.minutes > other.minutes
    else:
      return self.counter < other.counter

  def is_dominated(self, mprs: Set[ResourceStatus]) -> bool:
      for mpr in mprs:
        if (
          mpr.resources.ore >= self.resources.ore
        ) and (
          mpr.resources.clay >= self.resources.clay
        ) and (
          mpr.resources.obsidian >= self.resources.obsidian
        ) and (
          mpr.guaranteed >= self.guaranteed
        ) and (
          (
            mpr.resources.ore != self.resources.ore
          ) or (
            mpr.resources.clay != self.resources.clay
          ) or (
            mpr.resources.obsidian != self.resources.obsidian
          )
        ):
          return True
      return False

class Solution(SolutionABC):
  def __init__(
    self,
  ):
    self.blueprints: List[Blueprint] = []

  def parse_row(
    self,
    row: str,
  ):
    if len(self.blueprints) < BLUEPRINTS:
      self.blueprints.append(Blueprint(row))

  def solve(
    self,
  ) -> int:
    return math.prod(b.most_geodes() for b in self.blueprints)