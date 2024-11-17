# My first attempt at a CPU emulator in python
from typing import List
from enum import Enum, auto

class I(Enum): # Enum for more convenient access, changes and reverse lookup built in
    VAL = auto()
    MEM = auto()
    MOV = auto()
    ADD = auto()
    SUB = auto()
    MUL = auto()
    DIV = auto()
    CMP = auto()
    JMP = auto()
    JMPE = auto()
    JMPG = auto()
    JMPL = auto()
    OUT = auto()
    STOP = auto()
    
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
        return self._registers[idx.value]

    def exec(self):
        self._ip = 0 
        stopped = False
        while(not stopped):
            instruction = self.next_instruction()
            match instruction:
                case I.MOV:
                    src = self.next_instruction()
                    if (src == I.VAL):
                        src = self.next_instruction()
                    elif (src == I.MEM):
                        src = self._memory[self.next_instruction()]
                    else:
                        src = self.r(src)
                    dest = self.next_instruction()
                    if (dest == I.MEM):
                        self._memory[self.next_instruction()] = src
                    else:
                        self.r(dest)(src)
                case I.STOP:
                    stopped = True

if __name__ == "__main__":
    memory = [
        I.MOV,
        I.VAL,
        37,
        R.G2,
        I.STOP,
    ] + [0]*32
    c = CPU(memory)
    c.exec()
    print(c._registers[R.G2.value]())



