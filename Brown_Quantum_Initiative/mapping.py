from braket.circuits import Circuit

from edge_coloring import color_edges_of_complete_graph

QUBITS = 11


def init_noise_test_circuits(noise_model) -> list[Circuit]:
    edge_colorings = color_edges_of_complete_graph(QUBITS)
    circuits = []
    for edge_coloring in edge_colorings.values():
        circuit = Circuit()
        for qi, qj in edge_coloring:
            circuit.h(qi).cnot(qi, qj)
        qubits_used = sorted(circuit.qubits)
        for qi in range(len(qubits_used)):
            if int(qubits_used[qi]) != qi:
                circuit.x(qi)
                break
        noisy_circuit = noise_model.apply(circuit)
        circuits.append(noisy_circuit)
    return circuits


def fidelity_function(pair_count: dict):
    min_00_11 = min(pair_count["00"], pair_count["11"])
    max_00_11 = max(pair_count["00"], pair_count["11"])
    count_00_11 = min_00_11 + max_00_11
    total_count = (
        pair_count["00"] + pair_count["11"] + pair_count["10"] + pair_count["01"]
    )
    return min_00_11 / max_00_11 * count_00_11 / total_count


def calculate_2q_fidelity_dict(pair_counts: dict[tuple : dict[str:int]]) -> dict:
    fidelity = dict()
    for pair in pair_counts:
        fidelity[pair] = fidelity_function(pair_count=pair_counts[pair])
    return fidelity


def fidelity_function_single_gate(single_qubit_count):
    count_0, count_1 = single_qubit_count["0"], single_qubit_count["1"]
    return count_1 / (count_0 + count_1)


def calculate_1q_fidelity_dict(
    single_qubit_counts: dict[tuple : dict[str:int]],
) -> dict:
    fidelity = dict()
    for qubit in single_qubit_counts:
        fidelity[qubit] = fidelity_function_single_gate(
            single_qubit_count=single_qubit_counts[qubit]
        )
    return fidelity


def new_fidelity_2qubit_gates(counts, circuit) -> dict:
    # Initialize a dictionary to keep track of CNOT occurrences
    pair_counts = dict()
    # Iterate through the operations in the circuit
    for instruction in circuit.instructions:
        # Check if the operation is a CNOT gate
        if instruction.operator.name == "CNot":
            # Get the qubits involved in the CNOT gate
            qubits = tuple(sorted([int(qubit) for qubit in instruction.target]))
            pair_counts[qubits] = {"00": 0, "11": 0, "01": 0, "10": 0}

    for count in counts.keys():
        for pair in pair_counts.keys():
            qi, qj = pair
            bi, bj = count[qi], count[qj]
            pair_counts[pair][f"{bi}{bj}"] += 1

    new_fidelity = calculate_2q_fidelity_dict(pair_counts)
    return new_fidelity


def new_fidelity_1qubit_gates(counts, circuit):
    # Initialize a dictionary to keep track of CNOT occurrences
    single_qubit_counts = dict()
    # Iterate through the operations in the circuit
    for instruction in circuit.instructions:
        # Check if the operation is a CNOT gate
        if instruction.operator.name == "X":
            # Get the qubits involved in the CNOT gate
            qubit = int(instruction.target[0])
            single_qubit_counts[qubit] = {"0": 0, "1": 0}

    for count in counts.keys():
        for qi in single_qubit_counts.keys():
            bi = count[qi]
            single_qubit_counts[qi][f"{bi}"] += 1

    new_fidelity = calculate_1q_fidelity_dict(single_qubit_counts=single_qubit_counts)
    return new_fidelity


def gather_stats(noise_model, running_device, shots) -> dict:
    circuits = init_noise_test_circuits(noise_model)
    fidelity_2qubit_gates = dict()
    fidelity_1qubit_gates = dict()
    for circuit in circuits:
        counts = running_device.run(circuit, shots=shots).result().measurement_counts
        dict.update(fidelity_2qubit_gates, new_fidelity_2qubit_gates(counts, circuit))
        dict.update(fidelity_1qubit_gates, new_fidelity_1qubit_gates(counts, circuit))
    return fidelity_2qubit_gates


def calculate_counts_of_2q_gates(circuit):
    counts_2q = {}

    # Iterate through the operations in the circuit
    for instruction in circuit.instructions:
        # Check if the operation is a CNOT gate
        if instruction.operator.name in ["CNot", "CPhaseShift", "Swap"]:
            # Get the qubits involved in the CNOT gate
            qubits = tuple(sorted([int(qubit) for qubit in instruction.target]))
            # Increment the count for this pair of qubits in the dictionary
            if qubits in counts_2q:
                counts_2q[qubits] += 1
            else:
                counts_2q[qubits] = 1

    counts_2q_items = sorted(counts_2q.items(), key=lambda x: x[1], reverse=True)
    return counts_2q_items


def find_missing_number(numbers):
    # Calculate the expected sum of the first 11 natural numbers
    n = QUBITS - 1
    expected_sum = n * (n + 1) // 2

    # Calculate the actual sum of the numbers in the list
    actual_sum = sum(numbers)

    # The missing number is the difference between the expected sum and the actual sum
    missing_number = expected_sum - actual_sum
    return missing_number


def create_logical_to_physical_mapping(circuit, stats) -> dict:
    counts_2q = calculate_counts_of_2q_gates(circuit)
    # Sort the logical qubit interactions in descending order of interaction frequency

    # Sort the CNOT fidelities in descending order
    sorted_cnot_fidelities = sorted(stats.items(), key=lambda x: x[1], reverse=True)

    # Initialize the mapping of logical qubits to physical qubits
    mapping = {}

    # Iterate over the sorted logical interactions and map them to the highest fidelity physical pairs
    for logical_pair, _ in counts_2q:
        for physical_pair, fidelity in sorted_cnot_fidelities:
            if all(q not in mapping for q in logical_pair) and all(
                p not in mapping.values() for p in physical_pair
            ):
                # Map logical qubits to physical qubits
                mapping[logical_pair[0]] = physical_pair[0]
                mapping[logical_pair[1]] = physical_pair[1]
                break  # Move to the next logical pair after a successful mapping

    logical = find_missing_number(mapping.keys())
    physical = find_missing_number(mapping.values())
    mapping[logical] = physical
    return [mapping[position] for position in range(QUBITS)]


# def generate_indices(K=11):
#     upper_indices = []
#     for i in range(K):
#         for j in range(K):
#             if i < j:
#                 upper_indices.append((i, j))
#     return upper_indices


# def create_logical_to_physical_mapping(circuit, stats, num_trials=10000, N=11) -> tuple:
#     """
#     NOTE: this function assumes the counts dict has (i,j) AND (j,i) as keys
#     """
#     counts_2q = calculate_counts_of_2q_gates(circuit)
#     permutations = list(
#         itertools.permutations(np.arange(N))
#     )  # may want to run this outside of function
#     permutation_index = np.arange(len(permutations))
#
#     # find "best" permutation:
#     maximal_S = 0
#     indices = generate_indices()
#     best_permutation_index = None
#     dict_counts_2q = dict(counts_2q)
#     for i in range(num_trials):
#         p_i = np.random.choice(permutation_index)
#         s = 0
#         for i, j in indices:
#             ii, jj = permutations[p_i][i], permutations[p_i][j]
#             if ii < jj:
#                 s += stats[(i, j)] * dict_counts_2q[(ii, jj)]
#             else:
#                 s += stats[(i, j)] * dict_counts_2q[(jj, ii)]
#         if s > maximal_S:  # find largest sum over permutation space
#             maximal_S = s
#             best_permutation_index = p_i
#     return permutations[best_permutation_index]
