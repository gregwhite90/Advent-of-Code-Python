import re
import copy
import collections
from typing import Dict, Set, Counter

from shared import SolutionABC

LINE_RE = re.compile(r"(?P<foods>[\w ]+) \(contains (?P<allergens>[\w\, ]+)\)")

class Solution(SolutionABC):
  def __init__(
    self,
  ):
    self._allergen_to_ingredients: Dict[str, Set[str]] = {}
    self._all_foods: Counter[str] = collections.Counter()

  def parse_row(
    self,
    row: str,
  ):
    m = LINE_RE.match(row)
    assert m
    foods = set(m['foods'].split(' '))
    self._all_foods.update(foods)
    allergens = m['allergens'].split(', ')
    for allergen in allergens:
      if allergen in self._allergen_to_ingredients:
        self._allergen_to_ingredients[allergen] &= foods
      else:
        self._allergen_to_ingredients[allergen] = copy.copy(foods)

  def dedupe_allergen_to_ingredients(self):
    deduped: Set[str] = set()
    while sum(len(foods) for foods in self._allergen_to_ingredients.values()) > len(self._allergen_to_ingredients):
      for allergen, foods in self._allergen_to_ingredients.items():
        if len(foods) == 1 and allergen not in deduped:
          for other_allergen, other_foods in self._allergen_to_ingredients.items():
            if allergen == other_allergen:
              continue
            other_foods -= foods
          deduped.add(allergen)

  def dangerous_ingredients_list(self) -> str:
    allergens_and_ingredients = [(allergen, foods.pop()) for allergen, foods in self._allergen_to_ingredients.items()]
    allergens_and_ingredients.sort()
    return ','.join([ingredient for allergen, ingredient in allergens_and_ingredients])

  def solve(
    self,
  ) -> str:
    self.dedupe_allergen_to_ingredients()
    return self.dangerous_ingredients_list()