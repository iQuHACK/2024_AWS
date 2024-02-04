from braket.circuits import Circuit
from braket.devices import LocalSimulator


# circuitdsl start
def demo_circuit(circuit):
    circuit = circuit.x(0)
    circuit = circuit.x(0)

    return circuit


# circuitdsl end


def main():
    device = LocalSimulator()
    circuit = Circuit()
    demo = demo_circuit(circuit)
    print(device.run(demo, shots=100).result().measurement_counts)


if __name__ == "__main__":
    main()
