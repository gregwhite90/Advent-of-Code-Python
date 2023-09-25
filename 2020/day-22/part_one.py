import re
from collections import defaultdict, deque

if __name__ == '__main__':
  cur_player = None
  player_re = re.compile(r"Player (?P<id>\d)")
  decks = defaultdict(deque)
  with open('input/input.txt') as infile:
    for line in infile:
      if len(line.strip()) == 0:
        cur_player = None
        continue
      elif player_re.match(line.strip()):
        cur_player = player_re.match(line.strip())['id']
      else:
        decks[cur_player].append(int(line.strip()))
  while len(decks['1']) > 0 and len(decks['2']) > 0:
    card_1 = decks['1'].popleft()
    card_2 = decks['2'].popleft()
    if card_1 > card_2:
      decks['1'].append(card_1)
      decks['1'].append(card_2)
    else:
      decks['2'].append(card_2)
      decks['2'].append(card_1)
  score_1 = sum(decks['2'][i] * (len(decks['2'])- i) for i in range(len(decks['2'])))
  print(score_1)