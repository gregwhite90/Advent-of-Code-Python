import re
from collections import defaultdict
from typing import Union, NamedTuple, List, Dict, DefaultDict

from shared import SolutionABC

BUNDLE_RE = re.compile(r"(?P<quantity>\d+) (?P<chemical>[A-Z]+)")
NECESSARY_FUEL = 3000000

class Bundle(NamedTuple):
  chemical: str
  quantity: int

def str_to_bundle(raw: str) -> Bundle:
  m = BUNDLE_RE.match(raw)
  assert m
  return Bundle(m['chemical'], int(m['quantity']))

class Reaction:
  def __init__(
    self,
    output: Bundle,
    inputs: Dict[str, Bundle],
  ):
    self.output = output
    self.inputs = inputs

  def necessary_times(
    self,
    necessary_output_quantity: int,
  ) -> int:
    return ((self.output.quantity - 1) + necessary_output_quantity) // self.output.quantity

class OrePerFuelCalculator:
  def __init__(
    self,
    reactions: Dict[str, Reaction],
    chem_to_inputs: DefaultDict[str, List[str]],
    necessary_fuel: int,
  ):
    self.reactions = reactions
    self.chem_to_inputs = chem_to_inputs
    self.necessary_quantities: Dict[str, int] = {
      'FUEL': necessary_fuel,
    }

  def necessary_quantity(
    self,
    chemical: str,
  ) -> int:
    if chemical in self.necessary_quantities: return self.necessary_quantities[chemical]
    # todo: fix
    reactions = [self.reactions[chem] for chem in self.chem_to_inputs[chemical]]
    necessary = sum(
      reaction.necessary_times(
        self.necessary_quantity(reaction.output.chemical)
      ) * reaction.inputs[chemical].quantity
      for reaction in reactions
    )
    self.necessary_quantities[chemical] = necessary
    return necessary

class Solution(SolutionABC):
  def __init__(
    self,
  ):
    self.reactions: Dict[str, Reaction] = {}
    self.chem_to_inputs: DefaultDict[str, List[str]] = defaultdict(list)
    self.necessary_quantities: Dict[str, int] = {
      'FUEL': NECESSARY_FUEL,
    }

  def parse_row(
    self,
    row: str,
  ):
    inputs, output = row.split(" => ")
    inputs = inputs.split(", ")
    reaction = Reaction(
      str_to_bundle(output),
      {str_to_bundle(input).chemical: str_to_bundle(input) for input in inputs},
    )
    self.reactions[reaction.output.chemical] = reaction
    for input in reaction.inputs.keys():
      self.chem_to_inputs[input].append(
        reaction.output.chemical
      )

  def necessary_quantity(
    self,
    chemical: str,
  ) -> int:
    if chemical in self.necessary_quantities: return self.necessary_quantities[chemical]
    # todo: fix
    reactions = [self.reactions[chem] for chem in self.chem_to_inputs[chemical]]
    necessary = sum(
      reaction.necessary_times(
        self.necessary_quantity(reaction.output.chemical)
      ) * reaction.inputs[chemical].quantity
      for reaction in reactions
    )
    self.necessary_quantities[chemical] = necessary
    return necessary

  def solve(
    self,
  ) -> Union[int, str]:
    fuel = 2650000
    while True:
      calc = OrePerFuelCalculator(
        self.reactions,
        self.chem_to_inputs,
        fuel,
      )
      if calc.necessary_quantity('ORE') > 1000000000000:
        break
      else:
        fuel += 1
    return fuel - 1