from typing import Dict

from solutions.shared import SolutionABC

DECIMAL_PLACE_TO_SNAFU_DIGIT = {
  2: '2',
  1: '1',
  0: '0',
  -1: '-',
  -2: '=',
}

SNAFU_DIGIT_TO_DECIMAL_PLACE = {
  v: k for k, v in DECIMAL_PLACE_TO_SNAFU_DIGIT.items()
}

def snafu_to_decimal(snafu: str) -> int:
  return sum(
    (5 ** place) * SNAFU_DIGIT_TO_DECIMAL_PLACE[char]
    for place, char in enumerate(reversed(snafu))
  )

class Solution(SolutionABC):
  def __init__(
    self,
  ):
    self._max_snafus: Dict[int, int] = {
      0: 0,
    }
    self._running_dec_sum = 0

  def parse_row(
    self,
    row: str,
  ):
    self._running_dec_sum += snafu_to_decimal(row)

  def solve(
    self,
  ) -> str:
    return self._decimal_to_snafu(self._running_dec_sum)

  def _decimal_to_snafu(self, decimal: int) -> str:
    place = 1
    res = ''
    while decimal > self._max_snafu(place) or decimal < - self._max_snafu(place):
      place *= 5
    while place >= 1:
      for decimal_place, snafu_digit in DECIMAL_PLACE_TO_SNAFU_DIGIT.items():
        if decimal - decimal_place * place <= self._max_snafu(place // 5) and decimal - decimal_place * place >= - self._max_snafu(place // 5):
          res += snafu_digit
          decimal -= decimal_place * place
          place //= 5
          break
    return res

  def _max_snafu(self, place: int) -> int:
    if place not in self._max_snafus:
      self._max_snafus[place] = 2 * place + self._max_snafu(place // 5)
    return self._max_snafus[place]