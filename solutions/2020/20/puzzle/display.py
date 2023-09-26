import re

def display_puzzle(orientation_file, tiles):
    line_re = re.compile(r"(?P<id>\d+) (?P<rotations>\d+) (?P<flips>[0xy])")
    with open(orientation_file) as infile:
        for line in infile:
            line_match = line_re.match(line.strip())
            id = int(line_match['id'])
            rotations = int(line_match['rotations'])
            flips = line_match['flips']
            tiles[id].orient(rotations, flips)
            print(tiles[id])
