import re
from collections import defaultdict

DIRECTIONS = ['N', 'E', 'S', 'W']
TURNS = {'L', 'R'}
SLIDES = {'F'}

if __name__ == '__main__':
    instruction_re = re.compile(
        r"^(?P<instr>\w)(?P<amount>\d+)$"
    )
    direction_index = 1
    waypoint = defaultdict(int)
    waypoint[0] = 1
    waypoint[1] = 10
    
    p_one_distances = defaultdict(int)
    p_two_distances = defaultdict(int)
    all_instrs = set(DIRECTIONS).union(TURNS).union(SLIDES)
    with open('input/input.txt') as infile:
        for instruction_str in infile:
            instruction_match = instruction_re.match(instruction_str.strip())
            instr = instruction_match['instr']
            assert(instr in all_instrs)
            amount = int(instruction_match['amount'])
            if instr in set(DIRECTIONS):
                p_one_distances[instr] += amount
                dir_index = DIRECTIONS.index(instr)
                opposite_dir_index = (dir_index + 2) % len(DIRECTIONS)
                opposite_direction = DIRECTIONS[(DIRECTIONS.index(instr) + 2) % len(DIRECTIONS)]
                if waypoint[opposite_dir_index] > 0:
                    if waypoint[opposite_dir_index] > amount:
                        waypoint[opposite_dir_index] -= amount
                    else:
                        waypoint[dir_index] = (amount - waypoint[opposite_dir_index])
                        waypoint[opposite_dir_index] = 0
                else:
                    waypoint[dir_index] += amount
            elif instr in TURNS:
                assert(amount % 90 == 0)
                indices = amount // 90
                if instr == 'L': indices *= -1
                direction_index += indices
                direction_index %= len(DIRECTIONS)
                old_waypoint = waypoint
                waypoint = defaultdict(int)
                for old_dir_index, old_amt in old_waypoint.items():
                    waypoint[(old_dir_index + indices) % len(DIRECTIONS)] = old_amt
            elif instr == 'F':
                p_one_distances[DIRECTIONS[direction_index]] += amount
                for dir_index, distance in waypoint.items():
                    p_two_distances[DIRECTIONS[dir_index]] += (amount * distance)

    for distances in [p_one_distances, p_two_distances]:
        print(abs(distances['E'] - distances['W']) + abs(distances['N'] - distances['S']))
