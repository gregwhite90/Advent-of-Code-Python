from typing import List, Dict
from enum import Enum

class Opcode(Enum):
  ADD = 1
  MULTIPLY = 2
  INPUT = 3
  OUTPUT = 4
  JUMP_IF_TRUE = 5
  JUMP_IF_FALSE = 6
  LESS_THAN = 7
  EQUALS = 8
  HALT = 99

class ParameterMode(Enum):
  POSITION = 0
  IMMEDIATE = 1

PARAMETERS: Dict[Opcode, int] = {
  Opcode.ADD: 3,
  Opcode.MULTIPLY: 3,
  Opcode.INPUT: 1,
  Opcode.OUTPUT: 1,
  Opcode.JUMP_IF_TRUE: 2,
  Opcode.JUMP_IF_FALSE: 2,
  Opcode.LESS_THAN: 3,
  Opcode.EQUALS: 3,
  Opcode.HALT: 0,
}

OPCODE_DIGITS = 2

class OpcodeMode:
  def __init__(
    self,
    fullcode: int,
  ):
    fullcode_str = str(fullcode)
    self.opcode = Opcode(int(fullcode_str[-OPCODE_DIGITS:]))
    num_params = PARAMETERS[self.opcode]
    self.parameter_modes: List[ParameterMode] = [] 
    for param in range(num_params):
      if len(fullcode_str) > OPCODE_DIGITS + param:
        self.parameter_modes.append(ParameterMode(int(fullcode_str[-(OPCODE_DIGITS + param + 1)])))
      else:
        self.parameter_modes.append(ParameterMode(0))

class IntcodeComputer:
  def __init__(
    self,
    program: List[int],
  ):
    self.program = program

  def get_parameter(
    self,
    parameter_mode: ParameterMode,
    pointer: int,
  ) -> int:
    if parameter_mode == ParameterMode.IMMEDIATE:
      return self.program[pointer]
    else:
      assert parameter_mode == ParameterMode.POSITION
      return self.program[self.program[pointer]]

  def assert_writing_position_mode(
    self,
    opcode_mode: OpcodeMode,
  ):
    assert opcode_mode.parameter_modes[-1] == ParameterMode.POSITION

  def run(
    self,
  ):
    instruction_pointer = 0
    opcode_mode = OpcodeMode(self.program[instruction_pointer])
    while opcode_mode.opcode != Opcode.HALT:
      jumped = False
      if opcode_mode.opcode == Opcode.ADD:
        self.assert_writing_position_mode(opcode_mode)
        self.program[self.program[instruction_pointer + 3]] = (
          self.get_parameter(opcode_mode.parameter_modes[0], instruction_pointer + 1) + 
          self.get_parameter(opcode_mode.parameter_modes[1], instruction_pointer + 2)
        )
      elif opcode_mode.opcode == Opcode.MULTIPLY:
        self.assert_writing_position_mode(opcode_mode)
        self.program[self.program[instruction_pointer + 3]] = (
          self.get_parameter(opcode_mode.parameter_modes[0], instruction_pointer + 1) * 
          self.get_parameter(opcode_mode.parameter_modes[1], instruction_pointer + 2)
        )
      elif opcode_mode.opcode == Opcode.INPUT:
        self.assert_writing_position_mode(opcode_mode)
        self.program[self.program[instruction_pointer + 1]] = int(input())
      elif opcode_mode.opcode == Opcode.OUTPUT:
        print(self.get_parameter(opcode_mode.parameter_modes[0], instruction_pointer + 1))
      elif opcode_mode.opcode == Opcode.JUMP_IF_TRUE:
        if self.get_parameter(opcode_mode.parameter_modes[0], instruction_pointer + 1) != 0:
          instruction_pointer = self.get_parameter(
            opcode_mode.parameter_modes[1],
            instruction_pointer + 2,
          )
          jumped = True
      elif opcode_mode.opcode == Opcode.JUMP_IF_FALSE:
        if self.get_parameter(opcode_mode.parameter_modes[0], instruction_pointer + 1) == 0:
          instruction_pointer = self.get_parameter(
            opcode_mode.parameter_modes[1],
            instruction_pointer + 2,
          )
          jumped = True
      elif opcode_mode.opcode == Opcode.LESS_THAN:
        self.assert_writing_position_mode(opcode_mode)
        val = 1 if (
          self.get_parameter(opcode_mode.parameter_modes[0], instruction_pointer + 1) <
          self.get_parameter(opcode_mode.parameter_modes[1], instruction_pointer + 2)) else 0
        self.program[self.program[instruction_pointer + 3]] = val
      else:
        assert opcode_mode.opcode == Opcode.EQUALS          
        self.assert_writing_position_mode(opcode_mode)
        val = 1 if (
          self.get_parameter(opcode_mode.parameter_modes[0], instruction_pointer + 1) ==
          self.get_parameter(opcode_mode.parameter_modes[1], instruction_pointer + 2)) else 0
        self.program[self.program[instruction_pointer + 3]] = val

      if not jumped:
        instruction_pointer += PARAMETERS[opcode_mode.opcode] + 1
      opcode_mode = OpcodeMode(self.program[instruction_pointer])

  def position_0(self) -> int:
    return self.program[0]