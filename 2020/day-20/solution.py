import re
from collections import defaultdict

class Edge():
    def __init__(
            self,
            edge,
    ):
        self.edge = edge

    def to_key(
            self,
    ):
        if ''.join(self.edge) < ''.join(self.edge[::-1]):
            return (''.join(self.edge), ''.join(self.edge[::-1]))
        else:
            return (''.join(self.edge[::-1]), ''.join(self.edge))

    def __repr__(
            self,
    ):
        return ' or '.join(self.to_key())

class Tile():
    def __init__(
            self,
            id_num: int,
            lines,
    ):
        self.id_num = id_num
        self.lines = [list(line) for line in lines]
        self.edges = [
            Edge(lines[0]),
            Edge(lines[-1]),
            Edge([lines[i][0] for i in range(len(lines))]),
            Edge([lines[i][-1] for i in range(len(lines))]),
        ]

    def add_to_edges(
            self,
            edges,
    ):
        for edge in self.edges:
            edges[edge.to_key()].add(self.id_num)

    def get_edges(self):
        return self.edges

    def orient(
            self,
            rotations,
            flips,
    ):
        while (rotations % 4) > 0:
            self.rotate()
            rotations -= 1
        if flips == 'x':
            self.flip_x()
        elif flips == 'y':
            self.flip_y()

    def rotate(
            self,
    ):
        self.lines = rotate(self.lines)

    def flip_x(
            self,
    ):
        self.lines = flip_x(self.lines)

    def flip_y(
            self,
    ):
        self.lines = flip_y(self.lines)

    # TODO: clean up or delete
    def __repr__(self):
        tile_text = '\n'.join([''.join(self.lines[i]) for i in range(len(self.lines))])
        return (
            f"\nid: {self.id_num}\n"
            f"tile:\n"
            f"{tile_text}"
        )

def rotate(
        arr,
):
    return [[arr[len(arr) - 1 - i][j] for i in range(len(arr))] for j in range(len(arr))]

def flip_x(
        arr,
):
    return [arr[len(arr) - 1 - i] for i in range(len(arr))]

def flip_y(
        arr,
):
    return [arr[i][::-1] for i in range(len(arr))]

def default_id_and_lines():
    return None, []

def both_parts():

    # TODO: turn to enum
    tile_id_re = re.compile(r"^Tile (?P<id>\d+):$")
    tile_id, cur_lines = default_id_and_lines()
    tiles = {}
    edges = defaultdict(set)
    with open('input/input.txt') as input_file:
        cur_lines = []
        for line in input_file:
            l = line.strip()
            if len(l) == 0:
                tile = Tile(tile_id, cur_lines)
                tiles[tile_id] = tile
                tile.add_to_edges(edges)
                tile_id, cur_lines = default_id_and_lines()
            elif not tile_id:
                tile_id = int(tile_id_re.match(l)['id'])
            else:
                cur_lines.append(l)
        tile = Tile(tile_id, cur_lines)
        tiles[tile_id] = tile
        tile.add_to_edges(edges)

    unmatchable_edges = defaultdict(int)

    for edge, ids in edges.items():
        if len(ids) == 1:
            id = next(iter(ids))
            unmatchable_edges[id] += 1
    corners = set()
    for id, num in unmatchable_edges.items():
        if num == 2:
            corners.add(id)
    puzzle = get_puzzle('puzzle/orientation.txt', tiles, edges, unmatchable_edges)
    sms = find_sea_monsters(puzzle)
    print(f"total count of #: {puzzle.count('#')}")
    print(f"total count of # in sms: {sms * 15}")

def get_puzzle(orientation_file, tiles, edges, unmatchable_edges):
    line_re = re.compile(r"(?P<id>\d+) (?P<rotations>\d+) (?P<flips>[0xy])")
    pieces = []
    SIDE_LENGTH = 12
    with open(orientation_file) as infile:
        for line in infile:
            line_match = line_re.match(line.strip())
            id = int(line_match['id'])
            rotations = int(line_match['rotations'])
            flips = line_match['flips']
            tiles[id].orient(rotations, flips)
            pieces.append(tiles[id])
    puzzle = ''
    border = 1
    for row in range(SIDE_LENGTH):
        if row * SIDE_LENGTH >= len(pieces): break
        for i in range(border, len(pieces[row * SIDE_LENGTH].lines) - border):
            for col in range(SIDE_LENGTH):
                if row * SIDE_LENGTH + col >= len(pieces): break
                puzzle += ''.join(pieces[row * SIDE_LENGTH + col].lines[i][border:-border])
            puzzle += '\n'

    if len(pieces) % SIDE_LENGTH != 0:
        adjacent_pieces = defaultdict(set)
        for index in [-1, -SIDE_LENGTH]:
            for edge in pieces[index].get_edges():
                adjacent_pieces[index] = adjacent_pieces[index].union(edges[edge.to_key()])        
        idx = - SIDE_LENGTH

        next_piece = adjacent_pieces[-1].intersection(adjacent_pieces[-SIDE_LENGTH])
        next_piece.remove(pieces[-SIDE_LENGTH - 1].id_num)
    else:
        adjacent_pieces = set()
        for edge in pieces[-SIDE_LENGTH].get_edges():
            adjacent_pieces = adjacent_pieces.union(edges[edge.to_key()])
            next_piece = adjacent_pieces.intersection(set(unmatchable_edges.keys()))
        next_piece.remove(pieces[-SIDE_LENGTH].id_num)
        next_piece.remove(pieces[-2 * SIDE_LENGTH].id_num)
    return puzzle

def rotate_puzzle(puzzle):
    puzzle_arr = [list(line) for line in puzzle.strip().split('\n')]
    puzzle_arr = rotate(puzzle_arr)
    return '\n'.join(''.join(line) for line in puzzle_arr)

def flip_x_puzzle(puzzle):
    puzzle_arr = [list(line) for line in puzzle.strip().split('\n')]
    puzzle_arr = flip_x(puzzle_arr)
    return '\n'.join(''.join(line) for line in puzzle_arr)

def flip_y_puzzle(puzzle):
    puzzle_arr = [list(line) for line in puzzle.strip().split('\n')]
    puzzle_arr = flip_y(puzzle_arr)
    return '\n'.join(''.join(line) for line in puzzle_arr)    

def find_sea_monsters(puzzle):
    PUZZLE_LINE_CHARS = 12 * 8
    PUZZLE_LINE_LENGTH = PUZZLE_LINE_CHARS + 1 # for newline character
    assert(PUZZLE_LINE_LENGTH * PUZZLE_LINE_CHARS == len(puzzle))
    sea_monster_line_res = {
        0: re.compile(r"[\.#]{18}#[\.#]"),
        1: re.compile(r"#[\.#]{4}#{2}[\.#]{4}#{2}[\.#]{4}#{3}"),
        2: re.compile(r"[\.#]#([\.#]{2}#){5}[\.#]{3}"),
    }
    sm = []
    puzzle = flip_x_puzzle(puzzle)
    while len(sm) == 0:
        
        match = sea_monster_line_res[2].search(puzzle)
        while match:
            pos = match.start()
            row = pos // PUZZLE_LINE_LENGTH
            col = pos % PUZZLE_LINE_LENGTH
            if (
                    sea_monster_line_res[1].match(puzzle, (row - 1) * PUZZLE_LINE_LENGTH + col) and
                    sea_monster_line_res[0].match(puzzle, (row - 2) * PUZZLE_LINE_LENGTH + col)
            ):
                sm.append((row - 2, col))
            
            match = sea_monster_line_res[2].search(puzzle, pos + 1)
        if len(sm) > 0: break
        puzzle = rotate_puzzle(puzzle)

    return len(sm)

if __name__ == '__main__':
    both_parts()
    
