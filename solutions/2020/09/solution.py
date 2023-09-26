from collections import defaultdict
from typing import Dict, List, Tuple

PREAMBLE_LEN = 25

def pair_and_sum(
        nums: List[int],
        l_idx: int,
        r_idx: int,
) -> Tuple[Tuple[int, int], int]:
    return ((l_idx, r_idx), nums[l_idx] + nums[r_idx])

def num_is_valid(
        num: int,
        sum_to_pairs: Dict[int, Tuple[int, int]],
) -> bool:
    return len(sum_to_pairs[num]) >= 1

def process_num(
        index: int,
        nums: List[int],
        pair_to_sum: Dict[Tuple[int, int], int],
        sum_to_pairs: Dict[int, Tuple[int, int]],
) -> None:
    # TODO: implement
    i = index - 1
    while i > index - PREAMBLE_LEN and i >= 0:
        pair, s = pair_and_sum(nums, i, index)
        pair_to_sum[pair] = s
        sum_to_pairs[s].add(pair)
        i -= 1
    if index >= PREAMBLE_LEN:
        for j in range(index - PREAMBLE_LEN + 1, index):
            pair, s = pair_and_sum(nums, index - PREAMBLE_LEN, j)
            del pair_to_sum[pair]
            sum_to_pairs[s].remove(pair)

def find_contiguous_sum(
        sum_to_find: int,
        nums: List[int],
) -> int:
    start_idx = 0
    end_idx = 1
    max_plus_min = None
    while not max_plus_min:
        r = nums[start_idx:end_idx]
        cur_sum = sum(r)
        if cur_sum == sum_to_find:
            max_plus_min = max(r) + min(r)
        elif cur_sum > sum_to_find:
            start_idx += 1
        elif cur_sum < sum_to_find:
            end_idx += 1
    return max_plus_min

def both_parts():
    pair_to_sum = {}
    sum_to_pairs = defaultdict(set)

    with open('input/input.txt') as input_file:
        nums = [int(line.strip()) for line in input_file.readlines()]

    part_one = None

    for i, num in enumerate(nums):
        if i >= PREAMBLE_LEN:
            if not num_is_valid(num, sum_to_pairs): part_one = num
        process_num(i, nums, pair_to_sum, sum_to_pairs)

    part_two = find_contiguous_sum(part_one, nums)

    return part_one, part_two

if __name__ == '__main__':
    print(both_parts())
