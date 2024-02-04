from icuhack.circuit import Circuit, CNOT, Hadamard, X, Z, T
from icuhack.lexer import CircuitLexer, TopDefLexer


def parse_top_def(lexer, topdef: str):
    tokens = list(lexer.tokenize(topdef))
    name = None
    for tok in tokens:
        if tok.type == "ID":
            name = tok.value
        if tok.type == "LPAREN":
            break
    return name


def parse_gate(tokens):
    gate = tokens.pop(0)
    if gate.value == ".cnot":
        args = []
        for tok in tokens:
            if tok.type == "NUMBER":
                args.append(int(tok.value))
        control, target = args
        return CNOT(control, target)

    elif gate.value == ".h":
        args = []
        for tok in tokens:
            if tok.type == "NUMBER":
                args.append(int(tok.value))
        return Hadamard(args[0])

    elif gate.value == ".x":
        args = []
        for tok in tokens:
            if tok.type == "NUMBER":
                args.append(int(tok.value))
        return X(args[0])

    elif gate.value == ".z":
        args = []
        for tok in tokens:
            if tok.type == "NUMBER":
                args.append(int(tok.value))
        return Z(args[0])

    elif gate.value == ".t":
        args = []
        for tok in tokens:
            if tok.type == "NUMBER":
                args.append(int(tok.value))
        return T(args[0])


def parse_gate_expr(lexer, expr: str):
    tokens = list(lexer.tokenize(expr))
    parsed = None

    while tokens:
        tok = tokens[0]
        if tok.type == "GATE":
            parsed = parse_gate(tokens)
            break
        tokens.pop(0)

    return parsed


def extract_zxdsl(program: str):
    zxdsl = []
    program = program.split("\n")
    program = list(filter(lambda s: len(s) > 0, program))

    while line := program.pop(0):
        if line.strip() == "# circuitdsl start":
            break

    while line := program.pop(0):
        stripped = line.strip()
        if stripped == "# circuitdsl end":
            break
        else:
            zxdsl.append(stripped)

    return zxdsl


def parse(program_str: str):
    topdef_lexer = TopDefLexer()
    circuit_lexer = CircuitLexer()

    zxdsl_portion = extract_zxdsl(program_str)
    topdef = parse_top_def(topdef_lexer, zxdsl_portion.pop(0))

    program = []
    for line in zxdsl_portion:
        gate = parse_gate_expr(circuit_lexer, line)
        if gate:
            program.append(gate)

    return Circuit(topdef, program)
