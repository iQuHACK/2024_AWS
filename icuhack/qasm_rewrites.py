from typing import List


def add_inits(qasm: List[str], num_qubits: int):
    qasm_version = ["OPENQASM 3.0;"]
    reg_inits = [f"bit[{num_qubits}] b;", f"qubit[{num_qubits}] q;"]
    return qasm_version + [""] + reg_inits + [""] + qasm[3:]


def add_measures(qasm: List[str], num_qubits: int):
    measures = [f"b[{i}] = measure q[{i}];" for i in range(num_qubits)]
    return qasm + measures


def rewrite_cxs(qasm: List[str]):
    for i in range(len(qasm)):
        expr = qasm[i].split(" ")
        if expr[0] == "cx":
            qasm[i] = " ".join(["cnot"] + expr[1:]) 

    return qasm


def qasm_rewrites(qasm: List[str], num_qubits: int):
    rw1 = add_inits(qasm, num_qubits)
    rw2 = add_measures(rw1, num_qubits)
    rw3 = rewrite_cxs(rw1)
    return rw3
