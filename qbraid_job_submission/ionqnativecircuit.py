# Taken from the AWS tutorial, we added methods such as CNOT and identity

import numpy as np
from braket.circuits import Circuit, Gate


class IonQNativeCircuit(Circuit):
    pi = np.pi

    def __repr__(self) -> str:
        if not self.result_types:
            return f"IonQNativeCircuit('instructions': {self.instructions})"
        else:
            return (
                f"IonQNativeCircuit('instructions': {self.instructions}"
                + f", 'result_types': {self.result_types})"
            )

    def add_instruction(self, instruction, target=None, target_mapping=None):
        # Validate that only native gates are added to the circuit

        # qubit validation
        max_num_qubits = 25  # maximum number of qubits on Aria
        qubits = list(instruction.target)
        for qubit in qubits:
            if not (0 <= qubit < max_num_qubits):
                raise ValueError(
                    f"Qubit {qubit} is not in the valid range [0, {max_num_qubits}]."
                )

        # gate validation
        valid_gate_names = {Gate.GPi, Gate.GPi2, Gate.MS}
        gate_name = instruction.operator
        if not any(isinstance(gate_name, gate_cls) for gate_cls in valid_gate_names):
            raise ValueError(f"Gate {gate_name} is not in the valid gates.")

        return super().add_instruction(instruction, target, target_mapping)

    # universal single-qubit rotation decomposition
    def unitary(self, qubit, a, b, c):
        return self.gpi2(qubit, a).gpi(qubit, b).gpi2(qubit, c)

    def x(self, qubit):
        return self.gpi(qubit, 0)

    def i(self, qubit):
        return self.gpi(qubit, 0).gpi(qubit, 0)

    def y(self, qubit):
        return self.gpi(qubit, np.pi / 2)

    def z(self, qubit):
        return self.gpi(qubit, np.pi).gpi(qubit, np.pi / 2)

    def h(self, qubit):
        return self.gpi2(qubit, np.pi / 2).gpi(qubit, 0)

    def t(self, qubit):
        return self.unitary(qubit, 11 * np.pi / 8, np.pi / 2, -3 * np.pi / 8)

    def s(self, qubit):
        return self.unitary(qubit, 5 * np.pi / 4, np.pi / 2, -pi / 4)

    def rx(self, qubit, theta):
        return self.unitary(qubit, np.pi / 2, theta / 2 + np.pi / 2, np.pi / 2)

    def ry(self, qubit, theta):
        return self.unitary(qubit, np.pi, theta / 2 + np.pi, np.pi)

    def rz(self, qubit, theta):
        return self.gpi(qubit, 0).gpi(qubit, theta / 2)

    def cnott(self, qubit0, qubit1):
        return (
            self.ry(qubit0, np.pi / 2)
            .ms(qubit0, qubit1, 0, 0)
            .rx(qubit0, -np.pi / 2)
            .rx(qubit1, -np.pi / 2)
            .ry(qubit0, -np.pi / 2)
        )

    # add friendly printing
    def to_unitary(self):
        return np.round(super().to_unitary(), 5)
