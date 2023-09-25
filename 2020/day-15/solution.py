import re
from collections import defaultdict

STARTING_NUMBERS = [0, 1, 4, 13, 15, 12, 16]
TARGET_NTH = 30000000

def both_parts():
    part_one_memory = defaultdict(list)
    index = 0
    last_num = None
    for num in STARTING_NUMBERS:
        part_one_memory[num].append(index)
        last_num = num
        index += 1
    while index < TARGET_NTH:
        assert(len(part_one_memory[last_num]) > 0)
        if len(part_one_memory[last_num]) == 1:
            num = 0
        else:
            nums = part_one_memory[last_num]
            num = nums[-1] - nums[-2]
            part_one_memory[last_num] = part_one_memory[last_num][-2:]
        part_one_memory[num].append(index)
        last_num = num
        index += 1

    return last_num

if __name__ == '__main__':
    print(both_parts())
