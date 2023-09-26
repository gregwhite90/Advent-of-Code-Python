import csv

def calculate_fuel(mass):
    return mass // 3 - 2

def both_parts():
    part_one_fuel = 0
    part_two_fuel = 0
    with open('input/input.csv') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            mass = int(row[0])
            fuel = calculate_fuel(mass)
            part_one_fuel += fuel
            while fuel > 0:
                part_two_fuel += fuel
                fuel = calculate_fuel(fuel)
    return part_one_fuel, part_two_fuel

if __name__ == '__main__':
    part_one, part_two = both_parts()
    print(part_one)
    print(part_two)
