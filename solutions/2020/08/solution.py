import re
from typing import List

class Line:
    def __init__(self, instruction, value):
        self.instruction = instruction
        self.value = value

    def flip(self):
        assert self.instruction in ['nop', 'jmp']
        if self.instruction == 'nop':
            return Line('jmp', self.value)
        elif self.instruction == 'jmp':
            return Line('nop', self.value)

class TermStatus:
    def __init__(
            self,
            accumulator,
            instruction_ptr,
            instructions_executed
    ):
        self.accumulator = accumulator
        self.instruction_ptr = instruction_ptr
        self.instructions_executed = instructions_executed

    def __repr__(self):
        return (
            f"acc:   {self.accumulator}\n" +
            f"i_ptr: {self.instruction_ptr}\n" +
            f"num_i: {len(self.instructions_executed)}"
        )

def execute_bootcode(lines: List[Line]) -> TermStatus:
    accumulator = 0
    instruction_ptr = 0
    instructions_executed = set()

    while (
            instruction_ptr not in instructions_executed and
            instruction_ptr < len(lines)
    ):
        instructions_executed.add(instruction_ptr)
        line = lines[instruction_ptr]
        instruction = line.instruction
        value = line.value
        assert instruction in ['nop', 'jmp', 'acc']
        
        if instruction == 'jmp':
            instruction_ptr += value
        elif instruction == 'nop':
            instruction_ptr += 1
        elif instruction == 'acc':
            accumulator += value
            instruction_ptr += 1

    return TermStatus(accumulator, instruction_ptr, instructions_executed)   

def both_parts():
    line_re = re.compile(r"^(?P<instruction>\w{3}) (?P<value>[\+\-]\d+)$")
    
    with open('input/input.txt') as input_file:
        lines = input_file.readlines()

    lines = [
        Line(
            line_re.match(line.strip())['instruction'],
            int(line_re.match(line.strip())['value'])
        ) for line in lines
    ]

    part_one = execute_bootcode(lines)

    for instruction_ptr in part_one.instructions_executed:
        if lines[instruction_ptr].instruction not in ['nop', 'jmp']: continue
        print(f"flipping instruction index {instruction_ptr}")
        lines_copy = [Line(line.instruction, line.value) for line in lines]
        lines_copy[instruction_ptr] = lines_copy[instruction_ptr].flip()
        part_two = execute_bootcode(lines_copy)
        if part_two.instruction_ptr == len(lines_copy): break

    return part_one, part_two

if __name__ == '__main__':
    print(both_parts())
