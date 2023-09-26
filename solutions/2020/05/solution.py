ROW_LEN = 7
COL_LEN = 3

MIN_ID = 0
MAX_ID = (2 ** ROW_LEN - 1) * 8 + (2 ** COL_LEN - 1)

def seat_id(row_num, col_num):
    return row_num * 8 + col_num

def both_parts():
    found_seat_ids = set()
    max_seat_id = 0
    with open('input/input.txt') as input_file:
        for row in input_file:
            ticket = row.strip()
            row_num = int(ticket[:ROW_LEN].replace('F', '0').replace('B', '1'), 2)
            col_num = int(ticket[ROW_LEN:].replace('L', '0').replace('R', '1'), 2)
            cur_seat_id = seat_id(row_num, col_num)
            found_seat_ids.add(cur_seat_id)
            max_seat_id = max([max_seat_id, cur_seat_id])
    all_seat_ids = set(range(MIN_ID, MAX_ID))
    unfound_seat_ids = all_seat_ids - found_seat_ids
    my_seat_id = None
    for s_id in unfound_seat_ids:
        if s_id - 1 in found_seat_ids and s_id + 1 in found_seat_ids:
            my_seat_id = s_id
            break
    return max_seat_id, my_seat_id

if __name__ == '__main__':
    print(both_parts())
