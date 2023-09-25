from enum import Enum

class Shape(Enum):
  ROCK = 1
  PAPER = 2
  SCISSORS = 3

class Outcome(Enum):
  LOSS = 0
  DRAW = 3
  WIN = 6

PLAYER_MAPPING = {
  Shape.ROCK: {
    Outcome.LOSS: Shape.SCISSORS,
    Outcome.DRAW: Shape.ROCK,
    Outcome.WIN:  Shape.PAPER,
  },
  Shape.PAPER: {
    Outcome.LOSS: Shape.ROCK,
    Outcome.DRAW: Shape.PAPER,
    Outcome.WIN:  Shape.SCISSORS,
  },
  Shape.SCISSORS: {
    Outcome.LOSS: Shape.PAPER,
    Outcome.DRAW: Shape.SCISSORS,
    Outcome.WIN:  Shape.ROCK,
  },
}

OPPONENT_MAPPING = {
  'A': Shape.ROCK,
  'B': Shape.PAPER,
  'C': Shape.SCISSORS,
}

OUTCOME_MAPPING = {
  'X': Outcome.LOSS,
  'Y': Outcome.DRAW,
  'Z': Outcome.WIN,
}

class Round:
  def __init__(self, line: str):
    opponent_str, outcome_str = line.split()
    self._opponent = OPPONENT_MAPPING[opponent_str]
    self._outcome = OUTCOME_MAPPING[outcome_str]

  def _player_points(self) -> int:
    return PLAYER_MAPPING[self._opponent][self._outcome].value

  def _outcome_points(self) -> int:
    return self._outcome.value

  def points(self) -> int:
    return self._player_points() + self._outcome_points()

class RPS:
  def __init__(self):
    self._rounds = []

  def add_round(self, round: Round):
    self._rounds.append(round)

  def points(self) -> int:
    return sum(round.points() for round in self._rounds)

def parse_input(filename: str) -> RPS:
  rps = RPS()
  with open(filename) as infile:
    for line in infile:
      rps.add_round(Round(line))
  return rps

if __name__ == '__main__':
  rps = parse_input('input.txt')
  print(rps.points())