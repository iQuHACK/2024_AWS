from icuhack.circuit import Circuit, CNOT, Hadamard, Z, X


def apply_rewrite(src, targ, program):
    for i in range(len(program)):
        x, y = program[i]
        nx, ny = x, y
        if x == src:
            nx = targ
        elif x == targ:
            nx = src

        if y == src:
            ny = targ
        elif y == targ:
            ny = src
        
        program[i] = nx, ny
    
    return program


def optimize(program, candidate_pairs):
    dont_touch = set()
    rewrites = {}
    for fixpoint in range(len(program)):
        fixed_pair = program[fixpoint]
        x, y = fixed_pair
        if (x in dont_touch) or (y in dont_touch):
            continue
        candidates = []
        for c, d in candidate_pairs.keys():
            if x == c:
                if (d not in dont_touch):
                    candidates.append((candidate_pairs[(c, d)], (d, y)))
            if y == d:
                if (c not in dont_touch):
                    candidates.append((candidate_pairs[(c, d)], (x, c)))
        if not candidates:
            continue
        
        candidates.sort()
        _, cand_pair = candidates[0]
        src, targ = cand_pair
        rewrites[src] = targ
        rewrites[targ] = src
        program = apply_rewrite(src, targ, program)
        
        dont_touch.add(src)
        dont_touch.add(targ)
        dont_touch.add(program[fixpoint][0])
        dont_touch.add(program[fixpoint][1])
    
    return program, rewrites


def qubit_placement_optimization(circuit, candidate_pairs):
    program = circuit.get_program()
    two_qubit_gates = []
    for gate in program:
        if isinstance(gate, CNOT):
            two_qubit_gates.append((gate.control, gate.target))
    
    if not two_qubit_gates:
        return circuit

    new_two_qubit_gates, rewrites = optimize(two_qubit_gates, candidate_pairs)

    new_program = []
    for gate in program:
        if isinstance(gate, CNOT):
            ctrl, targ = new_two_qubit_gates.pop(0)
            new_program.append(CNOT(ctrl, targ))
        elif isinstance(gate, Hadamard):
            new_program.append(Hadamard(gate.qubit))
        elif isinstance(gate, Z):
            new_program.append(Z(gate.qubit))
        elif isinstance(gate, X):
            new_program.append(X(gate.qubit))
    
    return Circuit(circuit.name, new_program)
