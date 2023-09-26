import csv
import re

def both_parts():
    wires = []
    with open('input/input.csv') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            wires.append(row)
    part_one(wires)
    part_two(wires)

def part_one(wires):
    entry_re = re.compile(r"(?P<dir>\w)(?P<steps>\d+)")
    locations = []
    for i, wire in enumerate(wires):
        position = [0, 0]
        total_steps = 0
        locations.append({})
        for segment in wire:
            res = entry_re.match(segment)
            assert res
            direction = res['dir']
            steps = int(res['steps'])
            position, total_steps = add_locations(locations[i], position, total_steps, direction, steps)

    intersections = set(locations[0].keys()).intersection(*[set(loc.keys()) for loc in locations[1:]])
    min_dist = min([abs(intersection[0]) + abs(intersection[1]) for intersection in intersections if intersection != (0, 0)])
    print(min_dist)
    
def part_two(wires):
    entry_re = re.compile(r"(?P<dir>\w)(?P<steps>\d+)")
    locations = []
    for i, wire in enumerate(wires):
        position = [0, 0]
        total_steps = 0
        locations.append({})
        for segment in wire:
            res = entry_re.match(segment)
            assert res
            direction = res['dir']
            steps = int(res['steps'])
            position, total_steps = add_locations(locations[i], position, total_steps, direction, steps)

    intersections = set(locations[0].keys()).intersection(*[set(loc.keys()) for loc in locations[1:]])
    min_steps = min([sum([loc[intersection] for loc in locations]) for intersection in intersections])
    print(min_steps)

def add_locations(locations, position, total_steps, direction, steps):
    assert direction in ['R', 'L', 'U', 'D']
    if direction == 'R':
        for step in range(1, steps + 1):
            new_pos = (position[0] + step, position[1])
            if new_pos not in locations: locations[new_pos] = total_steps + step
        position[0] += steps
    elif direction == 'L':
        for step in range(1, steps + 1):
            new_pos = (position[0] - step, position[1])
            if new_pos not in locations: locations[new_pos] = total_steps + step
        position[0] -= steps
    elif direction == 'U':
        for step in range(1, steps + 1):
            new_pos = (position[0], position[1] + step)
            if new_pos not in locations: locations[new_pos] = total_steps + step
        position[1] += steps
    elif direction == 'D':
        for step in range(1, steps + 1):
            new_pos = (position[0], position[1] - step)
            if new_pos not in locations: locations[new_pos] = total_steps + step
        position[1] -= steps

    return position, total_steps + steps
    
if __name__ == '__main__':
    both_parts()

