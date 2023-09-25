import re

def part_one():

    memory = {}
    mask_re = re.compile(r"^mask = (?P<mask_bits>[01X]+)$")
    cur_and_mask = None
    cur_or_mask = None
    mem_re = re.compile(r"^mem\[(?P<addr>\d+)\] = (?P<val>\d+)$")
    with open('input/input.txt') as input_file:
        for line in input_file:
            l = line.strip()
            mask_match = mask_re.match(l)
            if mask_match:
                cur_and_mask = int(mask_match['mask_bits'].replace('X', '1'), 2)
                cur_or_mask = int(mask_match['mask_bits'].replace('X', '0'), 2)
                continue
            mem_match = mem_re.match(l)
            assert(mem_match)
            memory[mem_match['addr']] = int(mem_match['val']) & cur_and_mask | cur_or_mask

    return sum(memory.values())

if __name__ == '__main__':
    print(part_one())
