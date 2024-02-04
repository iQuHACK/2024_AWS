from braket.circuits import Circuit
from braket.devices import LocalSimulator


# circuitdsl start
def error_correction_circuit(circuit):
    circuit = circuit.h(0)
    circuit = circuit.cnot(0, 1)
    return circuit


# circuitdsl end


def main():
    device = LocalSimulator()
    circuit = Circuit()
    error_correction = error_correction_circuit(circuit)
    print(device.run(error_correction, shots=100).result().measurement_counts)


if __name__ == "__main__":
    main()
