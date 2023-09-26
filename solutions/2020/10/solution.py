from collections import defaultdict
from typing import List, Dict

VALID_JUMPS = {1, 2 ,3}

def part_one(nums: List[int]) -> int:
    jumps = defaultdict(int)
    for i in range(1, len(nums)):
        jumps[nums[i] - nums[i - 1]] += 1
    assert set(jumps.keys()).issubset(VALID_JUMPS)    
    return jumps[1] * jumps[3]

def part_two(nums: List[int]) -> int:
    paths = {}    
    return num_paths(nums, 0, paths)

def num_paths(nums: List[int], index: int, paths: Dict[int, int]) -> int:
    if index not in paths:
        # populate paths[index]
        i = index + 1
        all_paths = 1 if index == len(nums) - 1 else 0
        while i < len(nums) and nums[i] - nums[index] in VALID_JUMPS:
            all_paths += num_paths(nums, i, paths)
            i += 1
        paths[index] = all_paths
    return paths[index]

def both_parts():
    with open('input/input.txt') as input_file:
        nums = [int(line.strip()) for line in input_file.readlines()]

    nums.sort()

    nums.insert(0, 0)
    nums.append(nums[-1] + 3)

    p_one = part_one(nums)
    p_two = part_two(nums)

    return p_one, p_two

if __name__ == '__main__':
    print(both_parts())
