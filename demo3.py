from braket.circuits import Circuit
from braket.devices import LocalSimulator

# zxdsl start
def demo_circuit(circuit): 
    circuit = circuit.x(0)
        
    return circuit
# zxdsl end


def main():
    device = LocalSimulator()
    circuit = Circuit()
    demo = demo_circuit(circuit)
    print(device.run(demo, shots=100).result().measurement_counts)


if __name__ == "__main__":
    main()
