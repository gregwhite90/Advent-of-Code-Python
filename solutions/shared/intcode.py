from collections import defaultdict
from typing import List, Dict, DefaultDict
from enum import Enum, auto

class Opcode(Enum):
  ADD = 1
  MULTIPLY = 2
  INPUT = 3
  OUTPUT = 4
  JUMP_IF_TRUE = 5
  JUMP_IF_FALSE = 6
  LESS_THAN = 7
  EQUALS = 8
  RELATIVE_BASE_OFFSET = 9
  HALT = 99

class ParameterMode(Enum):
  POSITION = 0
  IMMEDIATE = 1
  RELATIVE = 2

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
  Opcode.RELATIVE_BASE_OFFSET: 1,
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

class InputMode(Enum):
  INPUT = auto()
  CONNECTED = auto()

class IntcodeComputer:
  def __init__(
    self,
    program: List[int],
    inputs: List[int],
    input_modes: List[InputMode],
  ):
    self.program = program
    self.inputs = inputs
    self.input_modes = input_modes
    self.outputs: List[int] = []
    self.instruction_pointer = 0
    self.input_idx = 0
    self.relative_base = 0
    self.addl_memory: DefaultDict[int, int] = defaultdict(int)

  def read_parameter(
    self,
    parameter_mode: ParameterMode,
    pointer: int,
  ) -> int:
    if parameter_mode == ParameterMode.IMMEDIATE:
      return self.read_memory(pointer)
    elif parameter_mode == ParameterMode.POSITION:
      return self.read_memory(self.read_memory(pointer))
    else:
      assert parameter_mode == ParameterMode.RELATIVE
      return self.read_memory(self.relative_base + self.read_memory(pointer))

  def is_halted(self) -> bool:
    return OpcodeMode(self.program[self.instruction_pointer]).opcode == Opcode.HALT

  def write_parameter(
    self,
    parameter_mode: ParameterMode,
    pointer: int,
    val: int,
  ):
    assert parameter_mode != ParameterMode.IMMEDIATE
    if parameter_mode == ParameterMode.POSITION:
      self.write_memory(self.read_memory(pointer), val)
    else:
      assert parameter_mode == ParameterMode.RELATIVE
      self.write_memory(self.relative_base + self.read_memory(pointer), val)

  def read_memory(
    self,
    location: int,
  ) -> int:
    assert location >= 0
    if location < len(self.program):
      return self.program[location]
    else:
      return self.addl_memory[location]

  def write_memory(
    self,
    location: int,
    val: int,
  ):
    assert location >= 0
    if location < len(self.program):
      self.program[location] = val
    else:
      self.addl_memory[location] = val

  def enqueue_input(
    self,
    input: int,
  ):
    self.inputs.append(input)
    self.input_modes.append(InputMode.CONNECTED)

  def run(
    self,
  ):
    opcode_mode = OpcodeMode(self.program[self.instruction_pointer])
    while opcode_mode.opcode != Opcode.HALT:
      jumped = False
      if opcode_mode.opcode == Opcode.ADD:
        self.write_parameter(
          opcode_mode.parameter_modes[2],
          self.instruction_pointer + 3,
          (
            self.read_parameter(opcode_mode.parameter_modes[0], self.instruction_pointer + 1) + 
            self.read_parameter(opcode_mode.parameter_modes[1], self.instruction_pointer + 2)
          )
        )
      elif opcode_mode.opcode == Opcode.MULTIPLY:
        self.write_parameter(
          opcode_mode.parameter_modes[2],
          self.instruction_pointer + 3,
          (
            self.read_parameter(opcode_mode.parameter_modes[0], self.instruction_pointer + 1) * 
            self.read_parameter(opcode_mode.parameter_modes[1], self.instruction_pointer + 2)
          )
        )
      elif opcode_mode.opcode == Opcode.INPUT:
        if self.input_idx >= len(self.inputs): break
        if self.input_modes[self.input_idx] == InputMode.INPUT:
          val = int(input())
        else:
          assert self.input_modes[self.input_idx] == InputMode.CONNECTED
          val = self.inputs[self.input_idx]
        self.input_idx += 1
        self.write_parameter(
          opcode_mode.parameter_modes[0],
          self.instruction_pointer + 1,
          val
        )
      elif opcode_mode.opcode == Opcode.OUTPUT:
        self.outputs.append(self.read_parameter(opcode_mode.parameter_modes[0], self.instruction_pointer + 1))
      elif opcode_mode.opcode == Opcode.JUMP_IF_TRUE:
        if self.read_parameter(opcode_mode.parameter_modes[0], self.instruction_pointer + 1) != 0:
          self.instruction_pointer = self.read_parameter(
            opcode_mode.parameter_modes[1],
            self.instruction_pointer + 2,
          )
          jumped = True
      elif opcode_mode.opcode == Opcode.JUMP_IF_FALSE:
        if self.read_parameter(opcode_mode.parameter_modes[0], self.instruction_pointer + 1) == 0:
          self.instruction_pointer = self.read_parameter(
            opcode_mode.parameter_modes[1],
            self.instruction_pointer + 2,
          )
          jumped = True
      elif opcode_mode.opcode == Opcode.LESS_THAN:
        val = 1 if (
          self.read_parameter(opcode_mode.parameter_modes[0], self.instruction_pointer + 1) <
          self.read_parameter(opcode_mode.parameter_modes[1], self.instruction_pointer + 2)) else 0
        self.write_parameter(
          opcode_mode.parameter_modes[2],
          self.instruction_pointer + 3,
          val
        )
      elif opcode_mode.opcode == Opcode.EQUALS:          
        val = 1 if (
          self.read_parameter(opcode_mode.parameter_modes[0], self.instruction_pointer + 1) ==
          self.read_parameter(opcode_mode.parameter_modes[1], self.instruction_pointer + 2)) else 0
        self.write_parameter(
          opcode_mode.parameter_modes[2],
          self.instruction_pointer + 3,
          val
        )
      else:
        assert opcode_mode.opcode == Opcode.RELATIVE_BASE_OFFSET
        self.relative_base += self.read_parameter(opcode_mode.parameter_modes[0], self.instruction_pointer + 1)
      
      if not jumped:
        self.instruction_pointer += PARAMETERS[opcode_mode.opcode] + 1
      opcode_mode = OpcodeMode(self.program[self.instruction_pointer])

  def position_0(self) -> int:
    return self.program[0]

  def get_outputs(self) -> List[int]:
    return self.outputs