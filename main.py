# My first attempt at a CPU emulator in python
from typing import List
from enum import Enum, auto

class I(Enum): # Enum for more convenient access, changes and reverse lookup built in
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
    A1 = Register() # Argument 1
    A2 = Register() # Argument 2
    A3 = Register() # Argument 3
    A4 = Register() # Argument 4 
    G1 = Register() # General 1
    G2 = Register() # General 2
    G3 = Register() # General 3
    G4 = Register() # General 4
    R = Register() # Return

class CPU: 
    def __init__(self, memory : List[I]):
        self._memory = memory
        self._z = False
        self._lz = False
        self._gz = False
        
    def set_flags(self, a:int, b:int):
        self._z = a==b
        self._lz = b>a
        self._gz = b<a
    
    def exec(self):
        ip = 0 
        while(True):
            instruction = self._memory[ip]
            match instruction:
                case I.MOV:
                case I.STOP:
                    print("hi")
            ip+=1

if __name__ == "__main__":
    globals().update(I.__members__)
    memory = [
        I.MOV,
        I.STOP
    ]
    CPU(memory).exec()


