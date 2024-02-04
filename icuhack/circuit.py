from dataclasses import dataclass

from sly import Lexer


class Circuit:

    def __init__(self, name, program):
        self.name = name
        self.program = program

    def __str__(self):
        string = ""
        string += f"circuit: {self.name}\n"
        string += "program:\n"
        for expr in self.program:
            string += "  " + str(expr) + "\n"
        return string

    def get_name(self):
        return self.name

    def get_program(self):
        return self.program


@dataclass
class CNOT:
    control: int
    target: int

    def __str__(self):
        return f"CNOT control: {self.control} target: {self.target}"


@dataclass
class Hadamard:
    qubit: int

    def __str__(self):
        return f"HADAMARD input: {self.qubit}"

@dataclass
class Z:
    qubit: int

    def __str__(self):
        return f"Z input: {self.qubit}"

@dataclass
class X:
    qubit: int

    def __str__(self):
        return f"X input: {self.qubit}"
