from typing import List

from icuhack.circuit import Circuit, CNOT, Hadamard, X, Z, T


def get_topdef_again(name: str):
    return f"def {name}():"


def get_zxcalc_gate(gate_op) -> str:
    if isinstance(gate_op, CNOT):
        return '"CNOT"'
    elif isinstance(gate_op, Hadamard):
        return '"H"'
    elif isinstance(gate_op, X):
        return '"X"'
    elif isinstance(gate_op, Z):
        return '"Z"'
    elif isinstance(gate_op, T):
        return '"T"'


def gate_op_to_zxcalc(gate_op) -> List[str]:
    add_gate = lambda args: "circuit.add_gate(" + ", ".join(args) + ")"
    if isinstance(gate_op, CNOT):
        args = [get_zxcalc_gate(gate_op), str(gate_op.control), str(gate_op.target)]
        return [add_gate(args)]
    elif isinstance(gate_op, Hadamard):
        args = [get_zxcalc_gate(gate_op), str(gate_op.qubit)]
        return [add_gate(args)]
    elif isinstance(gate_op, Z):
        args = [get_zxcalc_gate(gate_op), str(gate_op.qubit)]
        return [add_gate(args)]
    elif isinstance(gate_op, T):
        args = [get_zxcalc_gate(gate_op), str(gate_op.qubit)]
        return [add_gate(args)]
    elif isinstance(gate_op, X):
        return [
            add_gate(['"H"', str(gate_op.qubit)]),
            add_gate(['"Z"', str(gate_op.qubit)]),
            add_gate(['"H"', str(gate_op.qubit)]),
        ]


def get_qubits(program) -> int:
    qubits = set()
    for gate_op in program:
        if isinstance(gate_op, CNOT):
            qubits.add(gate_op.control)
            qubits.add(gate_op.target)
        elif isinstance(gate_op, Hadamard):
            qubits.add(gate_op.qubit)
        elif isinstance(gate_op, X):
            qubits.add(gate_op.qubit)
        elif isinstance(gate_op, Z):
            qubits.add(gate_op.qubit)
        elif isinstance(gate_op, T):
            qubits.add(gate_op.qubit)
    return qubits


def add_assign(op: str) -> str:
    return f"circuit = {op}"


def indent(body: List[str]) -> List[str]:
    return list(map(lambda line: f"    {line}", body))


def to_zxcalc(circuit: Circuit) -> str:
    topdef = get_topdef_again(circuit.get_name())

    program = circuit.get_program()
    zx_ops = []
    for op in program:
        zx_ops += gate_op_to_zxcalc(op)
    num_qubits = len(get_qubits(program))

    zx_body = [f"circuit = zx.Circuit({num_qubits})"] + zx_ops + ["return circuit"]

    zx_program = [topdef] + indent(zx_body)

    return zx_program


def zxcalc_reducer() -> List[str]:
    func_def = "def reduce_zx(circuit):"
    func_body = [
        "graph = circuit.to_graph()",
        "test_graph = graph.copy()",
        "test_graph = zx.teleport_reduce(test_graph, quiet=False)",
        "if circuit.verify_equality(zx.Circuit.from_graph(graph))==True:",
        "     print('verified!')",
        "c1 = zx.extract_circuit(graph).to_basic_gates()",
        "c1 = c1.stats()",
        'c1_parsed = c1.split("\\n")',
        "print('T-count BEFORE reduction:  ' + c1_parsed[1][8])",
        "graph = zx.teleport_reduce(graph, quiet=False)",
        "c2 = zx.extract_circuit(graph).to_basic_gates()",
        "c2 = c2.stats()",
        'c2_parsed = c2.split("\\n")',
        "print('T-count AFTER reduction:  ' + c2_parsed[1][8])",
        "c_opt = zx.extract_circuit(graph.copy())",
        "return c_opt",
    ]
    func = [func_def] + indent(func_body)
    return func


def zxcalc_to_qasm() -> List[str]:
    func_def = "def to_qasm(circuit):"
    func_body = "return circuit.to_basic_gates().to_qasm()"
    func = [func_def] + indent([func_body])
    return func


def zxcalc_gen_qasm_postprocess() -> List[str]:
    return [
        "def zxcalc_gen_qasm_postprocess(qasm, num_qubits):",
        '    qasm_lines = qasm.split("\\n")',
        "    for i in range(len(qasm_lines)):",
        '        if "qelib" in qasm_lines[i]:',
        '            qasm_lines[i] = ""',
        "    qasm_lines = qasm_rewrites(qasm_lines, num_qubits)",
        '    return "\\n".join(qasm_lines)',
    ]


def zxcalc_main_execution(circuit: Circuit) -> List[str]:
    func_def = "def main():"
    func_body = [
        "device = LocalSimulator()",
        f"circuit = {circuit.get_name()}()",
        f"num_qubits = {len(get_qubits(circuit.get_program()))}",
        "reduced = reduce_zx(circuit)",
        "program_qasm = to_qasm(circuit)",
        "qasm = zxcalc_gen_qasm_postprocess(program_qasm, num_qubits)",
        "program = Program(source=qasm)",
        "result = device.run(program, shots=100).result()",
        "print(result.measurement_counts)",
    ]
    func = [func_def] + indent(func_body)
    return func


def python_main_block() -> List[str]:
    return ['if __name__ == "__main__":', "    main()"]


def zxcalc_imports() -> List[str]:
    return [
        "import pyzx as zx",
        "from icuhack.qasm_rewrites import qasm_rewrites",
        "from braket.ir.openqasm import Program",
        "from braket.devices import LocalSimulator",
    ]


def zxcalc_program(circuit: Circuit) -> List[str]:
    program = []

    program += zxcalc_imports()

    program += ["", ""]
    program += to_zxcalc(circuit)

    program += ["", ""]
    program += zxcalc_reducer()

    program += ["", ""]
    program += zxcalc_to_qasm()

    program += ["", ""]
    program += zxcalc_gen_qasm_postprocess()

    program += ["", ""]
    program += zxcalc_main_execution(circuit)

    program += ["", ""]
    program += python_main_block()

    return "\n".join(program)
