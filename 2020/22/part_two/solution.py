import copy
from typing import List, Set, Tuple

from shared import SolutionABC

class RecursiveCombatGame:
  def __init__(
    self,
    hands: List[List[int]]
  ):
    self._starting_hands_seen: Set[Tuple[Tuple[int], Tuple[int]]] = set()
    self._hands = hands
    self._winner_idx: int = None

  def _play_round(self):
    hands_tuple = (tuple(self._hands[0]), tuple(self._hands[1]))
    if hands_tuple in self._starting_hands_seen:
      self._winner_idx = 0
      return
    self._starting_hands_seen.add(hands_tuple)
    cards = (self._hands[0].pop(0), self._hands[1].pop(0))
    round_winner = None
    if len(self._hands[0]) >= cards[0] and len(self._hands[1]) >= cards[1]:
      round_winner = RecursiveCombatGame([
        copy.copy(self._hands[0][:cards[0]]),
        copy.copy(self._hands[1][:cards[1]]),
      ]).winner()
    else:
      if cards[0] > cards[1]:
        round_winner = 0
      else:
        round_winner = 1
    # add the cards to the winner's hand
    self._hands[round_winner].append(cards[round_winner])
    self._hands[round_winner].append(cards[1 - round_winner])
    # check for a win
    if len(self._hands[0]) == 0:
      self._winner_idx = 1
    elif len(self._hands[1]) == 0:
      self._winner_idx = 0

  def winner(self) -> int:
    while self._winner_idx is None:
      self._play_round()
    return self._winner_idx

  def winner_score(self) -> int:
    assert self._winner_idx is not None
    return sum(card * (len(self._hands[self._winner_idx]) - i) for i, card in enumerate(self._hands[self._winner_idx]))

class Solution(SolutionABC):
  def __init__(
    self,
  ):
    self._player_idx = -1
    self._hands: List[List[int]] = [[], []]

  def parse_row(
    self,
    row: str,
  ):
    if row[:len('Player')] == 'Player':
      self._player_idx += 1
    elif len(row) > 0:
      self._hands[self._player_idx].append(int(row))

  def solve(
    self,
  ) -> int:
    game = RecursiveCombatGame(self._hands)
    game.winner()
    return game.winner_score()