import copy
from collections import defaultdict
from typing import List, Tuple, Dict, Set

# TODO: fix directionality
# TODO: abstract common functionality and directions to classes
# TODO: only do each directional search once.

def process_seen(seats: List[List[str]]) -> Dict[Tuple[int, int], Set[Tuple[int, int]]]:
    seen = defaultdict(set)
    max_radius = max([len(seats), len(seats[0])])
    for i in range(len(seats)):
        for j in range(len(seats[0])):
            if seats[i][j] == '.': continue
            searched = {
                'l': False,
                'ul': False,
                'u': False,
                'ur': False,
                'r': False,
                'dr': False,
                'd': False,
                'dl': False,
            }
            for radius in range(1, max_radius):
                if all(searched.values()): break
                if not searched['l']:
                    if i - radius >= 0:
                        if seats[i - radius][j] != '.':
                            searched['l'] = True
                            seen[(i, j)].add((i - radius, j))
                    else:
                        searched['l'] = True
                if not searched['ul']:
                    if i - radius >= 0 and j - radius >= 0:
                        if seats[i - radius][j - radius] != '.':
                            searched['ul'] = True
                            seen[(i, j)].add((i - radius, j - radius))
                    else:
                        searched['ul'] = True
                if not searched['u']:
                    if j - radius >= 0:
                        if seats[i][j - radius] != '.':
                            searched['u'] = True
                            seen[(i, j)].add((i, j - radius))
                    else:
                        searched['u'] = True
                if not searched['ur']:
                    if i + radius < len(seats) and j - radius >= 0:
                        if seats[i + radius][j - radius] != '.':
                            searched['ur'] = True
                            seen[(i, j)].add((i + radius, j - radius))
                    else:
                        searched['ur'] = True
                if not searched['r']:
                    if i + radius < len(seats):
                        if seats[i + radius][j] != '.':
                            searched['r'] = True
                            seen[(i, j)].add((i + radius, j))
                    else:
                        searched['r'] = True
                if not searched['dr']:
                    if i + radius < len(seats) and j + radius < len(seats[0]):
                        if seats[i + radius][j + radius] != '.':
                            searched['dr'] = True
                            seen[(i, j)].add((i + radius, j + radius))
                    else:
                        searched['dr'] = True
                if not searched['d']:
                    if j + radius < len(seats[0]):
                        if seats[i][j + radius] != '.':
                            searched['d'] = True
                            seen[(i, j)].add((i, j + radius))
                    else:
                        searched['d'] = True
                if not searched['dl']:
                    if i - radius >= 0 and j + radius < len(seats[0]):
                        if seats[i - radius][j + radius] != '.':
                            searched['dl'] = True
                            seen[(i, j)].add((i - radius, j + radius))
                    else:
                        searched['dl'] = True
    return seen

def seen_occupied(seats: List[List[str]], i: int, j: int, seen: Dict[Tuple[int, int], Set[Tuple[int, int]]]) -> int:
    return sum(1 if seats[row][col] == '#' else 0 for row, col in seen[(i, j)])

def adjacent_occupied(seats: List[List[str]], i: int, j: int) -> int:
    return (
        sum(
            sum(
                1 if seat == '#' else 0 for seat in row[max([j - 1, 0]):min([j + 2, len(row)])]
            ) for row in seats[max([0, i - 1]):min([i + 2, len(seats)])]
        )
        - (1 if seats[i][j] == '#' else 0)
    )

def iterate_part_one(seats: List[List[str]]) -> Tuple[List[List[str]], int]:
    seats_copy = copy.deepcopy(seats)
    changed = 0
    for i in range(len(seats)):
        for j in range(len(seats[0])):
            if seats[i][j] == 'L' and adjacent_occupied(seats, i, j) == 0:
                changed += 1
                seats_copy[i][j] = '#'
            elif seats[i][j] == '#' and adjacent_occupied(seats, i, j) >= 4:
                changed += 1
                seats_copy[i][j] = 'L'
    return seats_copy, changed

def iterate_part_two(seats: List[List[str]], seen) -> Tuple[List[List[str]], int]:
    seats_copy = copy.deepcopy(seats)
    changed = 0
    for i in range(len(seats)):
        for j in range(len(seats[0])):
            if seats[i][j] == 'L' and seen_occupied(seats, i, j, seen) == 0:
                changed += 1
                seats_copy[i][j] = '#'
            elif seats[i][j] == '#' and seen_occupied(seats, i, j, seen) >= 5:
                changed += 1
                seats_copy[i][j] = 'L'
    return seats_copy, changed

def total_occupied(seats):
    return sum(
        sum(
            1 if seat == '#' else 0 for seat in row
        ) for row in seats
    )

def both_parts():
    with open('input/input.txt') as input_file:
        raw_seats = [list(line.strip()) for line in input_file.readlines()]

    seats = copy.deepcopy(raw_seats)
    num_changed = 1
    while num_changed > 0:
        seats, num_changed = iterate_part_one(seats)

    p_one = total_occupied(seats)

    seats = copy.deepcopy(raw_seats)
    seen = process_seen(seats)
    num_changed = 1
    while num_changed > 0:
        seats, num_changed = iterate_part_two(seats, seen)

    p_two = total_occupied(seats)

    return p_one, p_two

if __name__ == '__main__':
    print(both_parts())
