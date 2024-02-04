from mapping import gather_stats, create_logical_to_physical_mapping
from noise_model import noise_model
from braket.circuits import Circuit, Observable, Gate
from braket.devices import LocalSimulator
from circuits import (
    create_deep_cnot_circuit,
    create_deep_cnot_circuit_with_mapping,
    append_qft_circuit_with_mapping,
    append_inverse_qft_circuit,
    append_inverse_qft_circuit_with_mapping,
    append_qft_circuit,
)
from edge_coloring import color_edges_of_complete_graph
import numpy as np
import matplotlib.pyplot as plt

QUBITS = 11


if __name__ == "__main__":
    device = LocalSimulator("braket_dm")
    run_shots = 100000
    nm = noise_model()
    cnot_depth_range = np.arange(100, 200, 10)

    deep_cnot_success_rate = []
    deep_cnot_remapped_success_rate = []

    for cnot_depth in cnot_depth_range:
        deep_cnot_circuit = create_deep_cnot_circuit(cnot_depth=cnot_depth)
        deep_cnot_circuit = nm.apply(deep_cnot_circuit)
        result = (
            device.run(deep_cnot_circuit, shots=run_shots).result().measurement_counts
        )
        deep_cnot_success_rate.append(result["00000000000"] / run_shots)

        stats = gather_stats(nm, device, shots=1000)
        logical_to_physical_mapping = create_logical_to_physical_mapping(
            circuit=deep_cnot_circuit, stats=stats
        )
        deep_cnot_circuit_with_remapping = create_deep_cnot_circuit_with_mapping(
            cnot_depth=cnot_depth, mapping=logical_to_physical_mapping
        )
        deep_cnot_circuit_with_remapping = nm.apply(deep_cnot_circuit_with_remapping)
        result = (
            device.run(deep_cnot_circuit_with_remapping, shots=run_shots)
            .result()
            .measurement_counts
        )
        deep_cnot_remapped_success_rate.append(result["00000000000"] / run_shots)

    fig, ax = plt.subplots(figsize=(8, 5), dpi=96)
    plt.plot(cnot_depth_range, deep_cnot_success_rate, label="without remapping")
    plt.plot(cnot_depth_range, deep_cnot_remapped_success_rate, label="with remapping")

    plt.xlabel("number of CNOT gates")
    plt.ylabel("success rate")
    plt.title(f"Deep CNOT circuit success rate")
    ax.legend(
        loc="upper right",
        fancybox=True,
        shadow=True,
        ncol=2,
    )

    plt.show()
