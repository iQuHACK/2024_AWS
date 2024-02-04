from pathlib import Path

import typer

from icuhack.parser import parse
from icuhack.zxcalc import zxcalc_program

app = typer.Typer()


def compiler_pipeline(source: str, outfile: str):
    # Parse circuitdsl
    program = parse(source)

    # Convert to ZX calc program that runs circuit qasm with Bracket
    zxprogram = zxcalc_program(program)
    with open(outfile, 'w') as f:
        f.write(zxprogram)


@app.command()
def main(filename: Path):
    outfile = filename.stem + "_compiled" + ".py"
    source = filename.read_text()
    compiler_pipeline(source, outfile)


if __name__ == "__main__":
    app()
