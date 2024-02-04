from pathlib import Path
from typing import Optional
from typing_extensions import Annotated
import json

import typer

from icuhack.parser import parse
from icuhack.zxcalc import zxcalc_program
from icuhack.qubit_placement import qubit_placement_optimization

app = typer.Typer()


def str_key_to_tuple(s):
    return tuple(json.loads(s))


def load_candidate_pair_json(candidate_pairs: str):
    loaded_data = {
        str_key_to_tuple(k): v
        for k, v in json.loads(candidate_pairs).items()
    }
    return loaded_data


def compiler_pipeline(source: str, outfile: str, candidate_pairs):
    # Parse source into circuitdsl
    circuit = parse(source)

    # Optimize qubit placement on circuitdsl
    if candidate_pairs:
        circuit = qubit_placement_optimization(circuit, candidate_pairs) 

    # Compile to ZX calc program that runs circuit qasm with Bracket
    zxprogram = zxcalc_program(circuit)

    # Emit final compiled program
    print(f"Compiled to {outfile}...")
    with open(outfile, 'w') as f:
        f.write(zxprogram)


@app.command()
def main(
    filename: Annotated[Path, typer.Argument()],
    candidate_pairs_json: Annotated[Optional[Path], typer.Argument()] = None
):
    outfile = filename.stem + "_compiled" + ".py"
    source = filename.read_text()
    candidate_pairs = None
    if candidate_pairs_json:
        candidate_pairs = load_candidate_pair_json(
            candidate_pairs_json.read_text()
        )

    compiler_pipeline(source, outfile, candidate_pairs)


if __name__ == "__main__":
    app()
