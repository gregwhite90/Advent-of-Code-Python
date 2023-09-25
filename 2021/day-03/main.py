import csv
import math

def read_to_list():
  nums = []
  with open('input.csv') as input_file:
    input_reader = csv.reader(input_file)
    for line_num, line in enumerate(input_reader):
      nums += [line[0]]
  return nums

def round_half_up(n, decimals=0):
  multiplier = 10 ** decimals
  return math.floor(n*multiplier + 0.5) / multiplier

def digit_commonality(nums):
  counts = [0 for _ in range(len(nums[0]))]
  for line_num, num in enumerate(nums):
    for digit_index, digit in enumerate(list(num)):
      counts[digit_index] += int(digit)
  # builtin round function rounds 0.5 down
  most_common_digits = [int(round_half_up(count / len(nums), 0)) for count in counts]
  least_common_digits = [1 - digit for digit in most_common_digits]  
  return most_common_digits, least_common_digits

def part_one():
  nums = read_to_list()
  most_common_digits, least_common_digits = digit_commonality(nums)
  gamma_digits = [str(digit) for digit in most_common_digits]
  epsilon_digits = [str(digit) for digit in least_common_digits]
  gamma = int(''.join(gamma_digits), 2)
  epsilon = int(''.join(epsilon_digits), 2)
  return gamma * epsilon

def filter_nums(nums, digit_commonality_fun):
  digit_index = 0
  while len(nums) > 1:
    digits = digit_commonality_fun(nums)
    nums = list(filter(
      lambda num: int(num[digit_index]) == digits[digit_index],
      nums
    ))    
    digit_index += 1
  return(nums)

def rating(digit_commonality_index):
  nums = read_to_list()
  nums = filter_nums(
    nums,
    lambda ns: digit_commonality(ns)[digit_commonality_index]
  )
  return int(nums[0], 2)  

def part_two():
  ogr = rating(0)
  csr = rating(1)
  return ogr * csr

if __name__ == '__main__':
  print(part_one())

  print(part_two())