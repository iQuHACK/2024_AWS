from icuhack.parser import parse

test = """
from braket.circuits import Circuit


# zxdsl start
def error_correction_circuit(circuit): 
    circuit = circuit.h(0)
    circuit = circuit.h(1)
    circuit = circuit.h(2)
    circuit = circuit.h(3)
    circuit = circuit.cnot(0, 4)
    circuit = circuit.cnot(2, 5)
    circuit = circuit.cnot(1, 4)
    circuit = circuit.cnot(3, 5)
    circuit = circuit.cnot(4, 6)
    circuit = circuit.cnot(5, 6)
        
    return circuit
# zxdsl end


def main():
    circuit = Circuit()
    error_correction = error_correction_circuit(circuit)
"""


def main():
    program = parse(test)
    print(program)


if __name__ == "__main__":
    main()
