from pathlib import Path

import typer

from icuhack.parser import parse
from icuhack.zxcalc import zxcalc_program
from icuhack.qubit_placement import qubit_placement_optimization

app = typer.Typer()

candidate_pairs = {
    (0, 3) : 10,
    (0, 4) : 15,
    (3, 5) : 10,
    (1, 7) : 10,
    (2, 6) : 10
}

def compiler_pipeline(source: str, outfile: str):
    # Parse source into circuitdsl
    circuit = parse(source)
    
    # Optimize qubit placement on circuitdsl
    qubit_optimized = qubit_placement_optimization(circuit, candidate_pairs) 

    # Compile to ZX calc program that runs circuit qasm with Bracket
    zxprogram = zxcalc_program(qubit_optimized)

    # Emit final compiled program
    with open(outfile, 'w') as f:
        f.write(zxprogram)


@app.command()
def main(filename: Path):
    outfile = filename.stem + "_compiled" + ".py"
    source = filename.read_text()
    compiler_pipeline(source, outfile)


if __name__ == "__main__":
    app()
