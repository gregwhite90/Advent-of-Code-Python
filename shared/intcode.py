from typing import List
from enum import Enum

INSTRUCTION_STEP = 4

class Opcode(Enum):
  ADD = 1
  MULTIPLY = 2
  HALT = 99

class IntcodeComputer:
  def __init__(
    self,
    program: List[int],
  ):
    self.program = program

  def run(
    self,
  ):
    instruction_pointer = 0
    opcode = Opcode(self.program[instruction_pointer])
    while opcode != Opcode.HALT:
      if opcode == Opcode.ADD:
        self.program[self.program[instruction_pointer + 3]] = (
          self.program[self.program[instruction_pointer + 1]] + 
          self.program[self.program[instruction_pointer + 2]]
        )
      else:
        assert opcode == Opcode.MULTIPLY
        self.program[self.program[instruction_pointer + 3]] = (
          self.program[self.program[instruction_pointer + 1]] * 
          self.program[self.program[instruction_pointer + 2]]
        )

      instruction_pointer += INSTRUCTION_STEP
      opcode = Opcode(self.program[instruction_pointer])

  def position_0(self) -> int:
    return self.program[0]