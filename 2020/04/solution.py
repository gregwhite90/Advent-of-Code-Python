import re

# TODO: actual function for the check

field_validity_checks = {
    'byr': re.compile(r"^(?P<byr>\d{4})$"),
    'iyr': re.compile(r"^(?P<iyr>\d{4})$"),
    'eyr': re.compile(r"^(?P<eyr>\d{4})$"),
    'hgt': re.compile(r"^(?P<hgt>\d+)(?P<units>(cm|in))$"),
    'hcl': re.compile(r"^(?P<hcl>#[0-9a-f]{6})$"),
    'ecl': re.compile(r"^(?P<ecl>(amb|blu|brn|gry|grn|hzl|oth))$"),
    'pid': re.compile(r"^(?P<pid>\d{9})$"),
}

def year_field_is_valid(passport, year_field, minimum, maximum):
    res = field_validity_checks[year_field].match(passport[year_field])
    if not res: return False
    if int(res[year_field]) < minimum or int(res[year_field]) > maximum: return False
    return True

# TODO: set up as lambda functions tied directly to the field?
def fields_are_valid(passport):
    if not year_field_is_valid(passport, 'byr', 1920, 2002): return False
    if not year_field_is_valid(passport, 'iyr', 2010, 2020): return False
    if not year_field_is_valid(passport, 'eyr', 2020, 2030): return False

    res = field_validity_checks['hgt'].match(passport['hgt'])
    if not res: return False
    if res['units'] == 'cm':
        if int(res['hgt']) < 150 or int(res['hgt']) > 193: return False
    elif res['units'] == 'in':
        if int(res['hgt']) < 59 or int(res['hgt']) > 76: return False

    res = field_validity_checks['hcl'].match(passport['hcl'])
    if not res: return False

    res = field_validity_checks['ecl'].match(passport['ecl'])
    if not res: return False

    res = field_validity_checks['pid'].match(passport['pid'])
    if not res: return False

    return True

def passport_is_valid(passport):
    passport_validity = {}
    required_keys = set(['byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid'])
    if set(passport.keys()).intersection(required_keys) == required_keys:
        passport_validity['part_one'] = 1
    else:
        passport_validity['part_one'] = 0
        passport_validity['part_two'] = 0
        return passport_validity
    # check for part two
    passport_validity['part_two'] = 1 if fields_are_valid(passport) else 0
    if passport_validity['part_two'] == 1:
        print('\nvalid passport:')
        for k, v in sorted(passport.items(), key=lambda x: x[0]):
            print(f"{k}: {v}")
    return passport_validity

def update_valid_passports(valid_passports, passport):
    passport_validity = passport_is_valid(passport)
    for part in ['part_one', 'part_two']:
        valid_passports[part] += passport_validity[part]

def both_parts():
    valid_passports = {
        'part_one': 0,
        'part_two': 0
    }
    with open('input/input.txt') as input_file:
        passport = {}
        for row in input_file:
            if len(row.strip()) == 0:
                update_valid_passports(valid_passports, passport)
                passport = {}
            else:
                data = row.strip()
                entries = data.split(' ')
                for entry in entries:
                    key, value = entry.split(':')
                    passport[key] = value
        # check last passport
        update_valid_passports(valid_passports, passport)
    return valid_passports

if __name__ == '__main__':
    print(both_parts())
