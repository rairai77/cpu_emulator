# GAMEPLAN:
# TODO: First, complete all instructions at a high level
# TODO: Convert to some sort of encoding scheme to encode instructions into bytes instead of enums so it's more realistic!
# TODO: Write an assembler
# TODO: Create an ALU

from typing import List
from enum import Enum, auto

class I(Enum): # Enum for more convenient access, changes and reverse lookup built in
    VAL     = auto() # HANDLED
    MEM     = auto() # HANDLED
    MOV     = auto() # HANDLED
    ADD     = auto() # HANDLED
    SUB     = auto() # HANDLED
    MUL     = auto() # HANDLED
    DIV     = auto() # HANDLED
    CMP     = auto() # HANDLED
    JMP     = auto() # HANDLED
    JMPE    = auto() # HANDLED
    JMPG    = auto() # HANDLED    
    JMPL    = auto() # HANDLED
    OUT     = auto() # HANDLED
    IN      = auto() # HANDLED
    STOP    = auto() # HANDLED
    
    def __call__(self):
        return self.value
    
class Register:
    def __init__(self):
        self._value = 0
    
    def set(self, value : int):
        self._value = value
        
    def get(self):
        return self._value

    def __call__(self, value = None):
        if value:
            self.set(value)
        return self.get()
    
class R(Enum): # Enum for more convenient access
    A1 = auto() # Argument 1
    A2 = auto() # Argument 2
    A3 = auto() # Argument 3
    A4 = auto() # Argument 4 
    G1 = auto() # General 1
    G2 = auto() # General 2
    G3 = auto() # General 3
    G4 = auto() # General 4
    R = auto() # Return

    def __call__(self):
        return self.value
    

class CPU: 
    def __init__(self, memory : List):
        self._memory = memory
        self._registers = [
            Register() for _ in range(len(list(R)))
        ]
        self._z = False
        self._lz = False
        self._gz = False
        self._ip = 0
        
    def set_flags(self, a:int, b:int):
        self._z = a==b
        self._lz = b>a
        self._gz = b<a
        
    def next_instruction(self):
        self._ip += 1
        return self._memory[self._ip - 1]
    
    def r(self, idx):
        return self._registers[idx.value-1]

    def load_src(self):
        src = self.next_instruction()
        if (src == I.VAL):
            src = self.next_instruction()
        elif (src == I.MEM):
            src = self._memory[self.next_instruction()]
        else:
            src = self.r(src)()
        return src

    def exec(self) -> List[int]:
        output = []
        self._ip = 0 
        stopped = False
        while(not stopped):
            instruction = self.next_instruction()
            match instruction:
                case I.MOV:
                    src = self.load_src()
                    dest = self.next_instruction()
                    if (dest == I.MEM):
                        self._memory[self.next_instruction()] = src
                    else:
                        self.r(dest)(src)
                case I.JMP:
                    self._ip = self.load_src()
                case I.ADD:
                    src = self.load_src()
                    dest = self.next_instruction()
                    if (dest == I.MEM):
                        self._memory[self.next_instruction()] += src
                    else:
                        self.r(dest)(self.r(dest)()+src)
                case I.SUB:
                    src = self.load_src()
                    dest = self.next_instruction()
                    if (dest == I.MEM):
                        self._memory[self.next_instruction()] -= src
                    else:
                        self.r(dest)(self.r(dest)()-src)
                case I.MUL:
                    src = self.load_src()
                    dest = self.next_instruction()
                    if (dest == I.MEM):
                        self._memory[self.next_instruction()] *= src
                    else:
                        self.r(dest)(self.r(dest)()*src)
                case I.DIV:
                    src = self.load_src()
                    dest = self.next_instruction()
                    if (dest == I.MEM):
                        self._memory[self.next_instruction()] //= src
                    else:
                        self.r(dest)(self.r(dest)()//src)
                case I.OUT:
                    src = self.load_src()
                    output.append(src)
                case I.CMP:
                    self.set_flags(self.load_src(), self.load_src())
                case I.JMPE:
                    src = self.load_src()
                    if (self._z):
                        self._ip = src
                case I.JMPG:
                    src = self.load_src()
                    if (self._gz):
                        self._ip = src
                case I.JMPL:
                    src = self.load_src()
                    if (self._lz):
                        self._ip = src
                case I.IN:
                    src = input()
                    dest = self.next_instruction()
                    if (dest == I.MEM):
                        self._memory[self.next_instruction()] = src
                    else:
                        self.r(dest)(src)
                case I.STOP:
                    stopped = True
        return output
            

if __name__ == "__main__":
    memory = [
        I.IN, R.A1, # 1
        I.IN, R.A2, # 3
        I.CMP, R.A1, R.A2, #6
        I.JMPG, I.VAL, 14, #9
        I.OUT, I.VAL, -1, #12
        I.STOP,           #13
        I.OUT, I.VAL, 1,
        I.STOP
    ] + [0]*200
    c = CPU(memory)
    output = c.exec()
    print(output)
    # for idx, register in enumerate(c._registers):
    #     print(R(idx+1), register())
    # print(c._memory)



