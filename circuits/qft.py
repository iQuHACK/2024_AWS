import numpy as np
from braket.circuits import Circuit


def append_qft_circuit(circuit, qubits):
    # Apply the QFT transformation
    for j in range(qubits):
        # Apply the Hadamard gate to the j-th qubit
        circuit.h(j)
        # Apply the controlled phase rotations
        for k in range(j + 1, qubits):
            # The angle for the controlled rotation
            angle = 2 * np.pi / (2 ** (k - j + 1))
            circuit.cphaseshift(k, j, angle)

    # Reverse the order of the qubits
    for qubit in range(qubits // 2):
        circuit.swap(qubit, qubits - qubit - 1)

    return circuit


def append_qft_circuit_with_mapping(circuit, qubits, mapping):
    # Apply the QFT transformation
    for j in range(qubits):
        # Apply the Hadamard gate to the j-th qubit
        circuit.h(mapping[j])
        # Apply the controlled phase rotations
        for k in range(j + 1, qubits):
            # The angle for the controlled rotation
            angle = 2 * np.pi / (2 ** (k - j + 1))
            circuit.cphaseshift(mapping[k], mapping[j], angle)

    # Reverse the order of the qubits
    for qubit in range(qubits // 2):
        circuit.swap(mapping[qubit], mapping[qubits - qubit - 1])

    return circuit


def append_inverse_qft_circuit(circuit: Circuit, qubits):
    # Reverse the order of the qubits first
    for qubit in range(qubits // 2):
        circuit.swap(qubit, qubits - qubit - 1)

    # Apply the inverse QFT transformation
    for j in range(qubits - 1, -1, -1):
        # Apply the controlled phase rotations in reverse order
        for k in range(qubits - 1, j, -1):
            # The angle for the controlled rotation, with a negative sign for the inverse
            angle = -2 * np.pi / (2 ** (k - j + 1))
            circuit.cphaseshift(k, j, angle)
        # Apply the Hadamard gate to the j-th qubit
        circuit.h(j)

    return circuit


def append_inverse_qft_circuit_with_mapping(circuit: Circuit, qubits, mapping: list):
    # Reverse the order of the qubits first
    for qubit in range(qubits // 2):
        circuit.swap(mapping[qubit], mapping[qubits - qubit - 1])

    # Apply the inverse QFT transformation
    for j in range(qubits - 1, -1, -1):
        # Apply the controlled phase rotations in reverse order
        for k in range(qubits - 1, j, -1):
            # The angle for the controlled rotation, with a negative sign for the inverse
            angle = -2 * np.pi / (2 ** (k - j + 1))
            circuit.cphaseshift(mapping[k], mapping[j], angle)
        # Apply the Hadamard gate to the j-th qubit
        circuit.h(mapping[j])

    return circuit
