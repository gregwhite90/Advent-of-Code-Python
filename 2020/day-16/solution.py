import re
import math
from collections import defaultdict

class FieldIndices():
    def __init__(
            self,
            fields,
            indices,
    ):
        self.unassigned_fields = fields
        self.unassigned_indices = indices
        self.fields_to_index_assignments = {}
        self.fields_to_possible_indices = {field: set(indices) for field in fields}
        self.indices_to_possible_fields = {index: set(fields) for index in indices}

    def num_assigned(
            self,
    ):
        return len(self.fields_to_index_assignments)

    def assign(
            self,
            field,
            index,
    ):
        self.fields_to_index_assignments[field] = index
        self.unassigned_fields.discard(field)
        self.unassigned_indices.discard(index)
        for f, indices in self.fields_to_possible_indices.items():
            if f == field: continue
            indices.discard(index)
        for i, fields in self.indices_to_possible_fields.items():
            if i == index: continue
            fields.discard(field)

    def exclude(
            self,
            field,
            index,
    ):
        if field in self.fields_to_index_assignments:
            assert(index == self.fields_to_index_assignments[field])
            return
        self.fields_to_possible_indices[field].discard(index)
        self.indices_to_possible_fields[index].discard(field)

    def cascade(
            self,
    ):
        unassigned_fields_copy = set(self.unassigned_fields)
        for field in unassigned_fields_copy:
            if len(self.fields_to_possible_indices[field]) == 1:
                (index,) = self.fields_to_possible_indices[field]
                self.assign(field, index)
        unassigned_indices_copy = set(self.unassigned_indices)
        for index in unassigned_indices_copy:
            if len(self.indices_to_possible_fields[index]) == 1:
                (field,) = self.indices_to_possible_fields[index]
                self.assign(field, index)
        if unassigned_fields_copy != self.unassigned_fields or unassigned_indices_copy != self.unassigned_indices:
            self.cascade()

    def departure_indices(
            self,
    ):
        return set([index for field, index in self.fields_to_index_assignments.items() if field[:len('departure')] == 'departure'])

def both_parts():

    field_re = re.compile(r"^(?P<field_name>.*): (?P<min_num_0>\d+)\-(?P<max_num_0>\d+) or (?P<min_num_1>\d+)\-(?P<max_num_1>\d+)$")
    # TODO: turn to enum
    mode = 'fields'
    field_valid_values = defaultdict(set)
    valid_values = set()
    errors = []
    fields = set()
    indices = None
    field_indices = None
    my_ticket = None
    with open('input/input.txt') as input_file:
        for line in input_file:
            l = line.strip()
            if len(l) == 0: continue
            if l == 'your ticket:':
                mode = 'your ticket'
                continue
            if l == 'nearby tickets:':
                mode = 'nearby tickets'
                continue

            if mode == 'fields':
                field_match = field_re.match(l)
                fields.add(field_match['field_name'])
                for num_pair_idx in [0, 1]:
                    for num in range(
                            int(field_match[f"min_num_{num_pair_idx}"]),
                            int(field_match[f"max_num_{num_pair_idx}"]) + 1
                    ):
                        valid_values.add(num)
                        field_valid_values[field_match['field_name']].add(num)
            elif mode == 'your ticket':
                nums = [int(num) for num in l.split(',')]
                indices = set(range(len(nums)))
                field_indices = FieldIndices(fields, indices)
                my_ticket = nums
            elif mode == 'nearby tickets':
                nums = [int(num) for num in l.split(',')]
                valid = True
                for num in nums:
                    if num not in valid_values:
                        errors.append(num)
                        valid = False
                if not valid: continue
                for i, num in enumerate(nums):
                    for field, valid_values in field_valid_values.items():
                        if num not in valid_values:
                            field_indices.exclude(field, i)
                            field_indices.cascade()
    return sum(errors), math.prod([my_ticket[index] for index in field_indices.departure_indices()])

if __name__ == '__main__':
    print(both_parts())
