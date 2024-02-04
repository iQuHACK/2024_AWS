from mapping import gather_stats, create_logical_to_physical_mapping
from noise_model import noise_model
from braket.circuits import Circuit
from braket.devices import LocalSimulator
from circuits import (
    append_qft_circuit_with_mapping,
    append_inverse_qft_circuit,
    append_inverse_qft_circuit_with_mapping,
    append_qft_circuit,
)

QUBITS = 11

if __name__ == "__main__":
    device = LocalSimulator("braket_dm")
    run_shots = 10000
    qft_depth = 2
    nm = noise_model()

    qft_circuit = Circuit()
    for _ in range(qft_depth):
        qft_circuit = append_qft_circuit(qubits=QUBITS, circuit=qft_circuit)
        qft_circuit = append_inverse_qft_circuit(qubits=QUBITS, circuit=qft_circuit)
    qft_circuit = nm.apply(qft_circuit)
    result = device.run(qft_circuit, shots=run_shots).result().measurement_counts
    print(result)

    qft_circuit_remapped = Circuit()
    stats = gather_stats(nm, device, shots=1000)
    logical_to_physical_mapping = create_logical_to_physical_mapping(
        circuit=qft_circuit, stats=stats
    )
    for _ in range(qft_depth):
        qft_circuit_remapped = append_qft_circuit_with_mapping(
            qubits=QUBITS,
            circuit=qft_circuit_remapped,
            mapping=logical_to_physical_mapping,
        )
        qft_circuit_remapped = append_inverse_qft_circuit_with_mapping(
            qubits=QUBITS,
            circuit=qft_circuit_remapped,
            mapping=logical_to_physical_mapping,
        )
    qft_circuit_remapped = nm.apply(qft_circuit_remapped)
    result = (
        device.run(qft_circuit_remapped, shots=run_shots).result().measurement_counts
    )
    print(result)
