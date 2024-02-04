from braket.circuits import Circuit
from braket.devices import LocalSimulator
from braket.circuits.serialization import IRType

# circuitdsl start
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
# circuitdsl end


def main():
    device = LocalSimulator()
    circuit = Circuit()
    error_correction = error_correction_circuit(circuit)
    qasm_ir = error_correction.to_ir(IRType.OPENQASM)
    print(device.run(error_correction, shots=100).result().measurement_counts)


if __name__ == "__main__":
    main()
