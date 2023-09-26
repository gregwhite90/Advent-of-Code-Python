import csv
import re

def part_one_is_valid(password, ch, minimum, maximum):
    count = password.count(ch)
    return 1 if count >= minimum and count <= maximum else 0

def part_two_is_valid(password, ch, minimum, maximum):
    count = 0
    if len(password) >= minimum and password[minimum - 1] == ch: count += 1
    if len(password) >= maximum and password[maximum - 1] == ch: count += 1
    return 1 if count == 1 else 0

def both_parts():
    valid_part_one = 0
    valid_part_two = 0
    line_re = re.compile(r"(?P<minimum>\d+)\-(?P<maximum>\d+) (?P<ch>\w): (?P<password>.*)")
    with open('input/input.csv') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            res = line_re.match(row[0])
            assert res
            minimum = int(res['minimum'])
            maximum = int(res['maximum'])
            valid_part_one += part_one_is_valid(res['password'], res['ch'], minimum, maximum)
            valid_part_two += part_two_is_valid(res['password'], res['ch'], minimum, maximum)
    return valid_part_one, valid_part_two

if __name__ == '__main__':
    part_one, part_two = both_parts()
    print(part_one)
    print(part_two)
