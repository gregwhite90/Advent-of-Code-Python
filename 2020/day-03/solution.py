def trees(rows, change_x, change_y):
    trees = 0
    row_len = len(rows[0])
    x_pos = 0
    y_pos = 0
    while y_pos < len(rows):
        if rows[y_pos][x_pos] == '#': trees += 1
        x_pos = (x_pos + change_x) % row_len
        y_pos = y_pos + change_y
    return trees    

def both_parts():
    with open('input/input.txt') as input_file:
        rows = [line.rstrip('\n') for line in input_file]
    trees_3_1 = trees(rows, 3, 1)
    trees_1_1 = trees(rows, 1, 1)
    trees_5_1 = trees(rows, 5, 1)
    trees_7_1 = trees(rows, 7, 1)
    trees_1_2 = trees(rows, 1, 2)
    return trees_3_1, trees_3_1 * trees_1_1 * trees_5_1 * trees_7_1 * trees_1_2

if __name__ == '__main__':
    part_one, part_two = both_parts()
    print(part_one)
    print(part_two)
