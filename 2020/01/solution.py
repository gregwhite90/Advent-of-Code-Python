import csv

def complement(num):
    return 2020 - num

def part_one():
    with open('input/input.csv') as csvfile:
        reader = csv.reader(csvfile)
        found = set()
        for row in reader:
            num = int(row[0])
            found.add(num)
            compl = complement(num)
            if compl in found:
                print(f"Number:     {num}")
                print(f"Complement: {compl}")
                print(f"Product:    {num * compl}")

def part_two():
    with open('input/input.csv') as csvfile:
        reader = csv.reader(csvfile)
        found = set()
        for row in reader:
            num = int(row[0])
            found.add(num)
    for num_0 in found:
        for num_1 in found:
            compl = 2020 - num_0 - num_1
            if 2020 - num_0 - num_1 in found:                
                print(f"Number 0: {num_0}")
                print(f"Number 1: {num_1}")
                print(f"Number 2: {compl}")    
                print(f"Product:  {num_0 * num_1 * compl}")    

if __name__ == '__main__':
    part_one()
    part_two()
