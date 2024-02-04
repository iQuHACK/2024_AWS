from braket.circuits import Circuit

QUBITS = 11


def create_deep_cnot_circuit(cnot_depth):
    circuit = Circuit()
    for i in range(0, QUBITS - 1, 2):
        circuit.cnot(i, i + 1)
    circuit.i(QUBITS - 1)
    for _ in range(cnot_depth - 1):
        circuit.cnot(0, 1)
    return circuit


def create_deep_cnot_circuit_with_mapping(cnot_depth, mapping):
    circuit = Circuit()
    for i in range(0, QUBITS - 1, 2):
        circuit.cnot(mapping[i], mapping[i + 1])
    circuit.i(mapping[QUBITS - 1])
    for _ in range(cnot_depth - 1):
        circuit.cnot(mapping[0], mapping[1])
    return circuit
