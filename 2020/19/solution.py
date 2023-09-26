import re
from typing import Dict, Set

from shared import SolutionABC

CHAR_RULE_RE = re.compile(r'(?P<id>\d+): "(?P<char>a|b)"')
SIMPLE_RULE_RE = re.compile(r'(?P<id>\d+): (?P<rules>[\d ]+)')
OR_RULE_RE = re.compile(r'(?P<id>\d+): (?P<rules_0>[\d ]+) \| (?P<rules_1>[\d ]+)')

class Rule:
  """
  A rule takes one of 3 forms: a specific character, a concatenation of other rules, or an
  OR combination of 2 options of concatenations of other rules.
  
  Attributes:
    id: An integer id for the rule.
    re: The regex pattern for the rule, once it can be resolved.
    rules: A list of list of other rules that make up this one.
      If length 1, this is a simple concatenation. If length 2, this is an or rule.
    resolved: A boolean for whether the regex pattern has been resolved.
    depends_upon: A set of rule ids that need to be resolved before this rule's
      regex pattern can be resolved.
  """
  def __init__(self, row: str):
    m = CHAR_RULE_RE.match(row)
    if m:
      self.id = int(m['id'])
      self.re = m['char']
      self.rules = None
      self.resolved = True
      self.depends_upon = set()
    else:
      m = OR_RULE_RE.match(row)
      if m:
        self.id = int(m['id'])
        self.re = None
        self.rules = [
          [int(r_0) for r_0 in m['rules_0'].split(' ')],
          [int(r_1) for r_1 in m['rules_1'].split(' ')],
        ]
        self.resolved = False
        self.depends_upon = set(self.rules[0]) | set(self.rules[1])
      else:
        m = SIMPLE_RULE_RE.match(row)
        assert m
        self.id = int(m['id'])
        self.re = None
        self.rules = [[int(r) for r in m['rules'].split(' ')]]
        self.resolved = False
        self.depends_upon = set(self.rules[0])
    
class Solution(SolutionABC):
  def __init__(
    self,
  ):
    self.parsing_rules = True
    self.rules: Dict[int, Rule] = {}
    self.resolved_rules: Set[int] = set()
    self.rule_0_messages = 0

  def resolve_rules(self):
    for rule in self.rules.values():
      rule.depends_upon -= self.resolved_rules      
    while len(self.rules) > len(self.resolved_rules):
      for rule in self.rules.values():
        if rule.resolved:
          continue
        if len(rule.depends_upon) == 0:
          # 2 new special-case self-referential rules for part 2.
          if rule.id == 8:
            rule.re = '((' + ''.join(self.rules[component_rule_id].re for component_rule_id in rule.rules[0]) + ')+)'
          elif rule.id == 11:
            # this is a crufty way to do it, just hard-coding the number of times it could come up.
            rule.re = '((' + '{1}'.join(self.rules[component_rule_id].re for component_rule_id in rule.rules[0]) + '{1})' + '|' + '(' + '{2}'.join(self.rules[component_rule_id].re for component_rule_id in rule.rules[0]) + '{2})' + '|' + '(' + '{3}'.join(self.rules[component_rule_id].re for component_rule_id in rule.rules[0]) + '{3})' + '|' + '(' + '{4}'.join(self.rules[component_rule_id].re for component_rule_id in rule.rules[0]) + '{4})' + '|' + '(' + '{5}'.join(self.rules[component_rule_id].re for component_rule_id in rule.rules[0]) + '{5})' + ')'
          # resolve the rule
          elif len(rule.rules) == 1:
            rule.re = '(' + ''.join(self.rules[component_rule_id].re for component_rule_id in rule.rules[0]) + ')'
          else:
            assert len(rule.rules) == 2
            rules_0 = '(' + ''.join(self.rules[component_rule_id].re for component_rule_id in rule.rules[0]) + ')'
            rules_1 = '(' + ''.join(self.rules[component_rule_id].re for component_rule_id in rule.rules[1]) + ')'
            rule.re = '(' + rules_0 + '|' + rules_1 + ')'

          # track the rule as resolved
          rule.resolved = True
          self.resolved_rules.add(rule.id)
          for potentially_dependent_rule in self.rules.values():
            if rule.id in potentially_dependent_rule.depends_upon:
              potentially_dependent_rule.depends_upon.remove(rule.id)

  def parse_row(
    self,
    row: str,
  ):
    if len(row) == 0:
      self.parsing_rules = False
      self.resolve_rules()
    elif self.parsing_rules:
      rule = Rule(row)
      self.rules[rule.id] = rule
      if rule.resolved:
        self.resolved_rules.add(rule.id)
    else:
      # parsing messages
      assert self.rules[0].resolved
      rule_0_re = re.compile(self.rules[0].re)
      if rule_0_re.fullmatch(row):
        self.rule_0_messages += 1
  
  def solve(
    self,
  ) -> int:
    return self.rule_0_messages