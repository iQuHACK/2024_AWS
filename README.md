# TEAM_iCuHack

Hello! We are Chris Yoon, Erica Choi, Kevin Park, Ha Yeon Kim, and Joey Koh.
We participated in AWS iQuHACK 2024 In-Person Challenge.
This is our repo and we have short slides about our noise aware compilation of
AWS Braket circuits.
[Link to our slides](https://docs.google.com/presentation/d/1j7Nu_adU32vfPOUmudidZ-MPrti-X4SPa5-mQk71t44/edit?usp=sharing)
Following the instructions below you will be able to test our compiler.

## Instructions
**First,"* fork the repo and open it in your terminal.

**Second,** activate your virtual enviornment to run poetry.
```
source .venv/bin/activate
```

**Third,** install `poetry` to install our package (our compiler) and its dependencies.
```
poetry install
```

**Finally,** using the following line of code you can test our compiler!
```
# Compile the demo circuit with our compiler
python compiler.py demo1.py candidate_pair.json

# Execute the compiled file with python
python demo1_compiled.py
```

In general,
```
python compiler.py <circuit>.py <optional candidate pair>.json

python <circuit>_compiled.py
```

If you'd like to print out the intermediate representations, you will have to edit the compiler.py file to print things like the CircuitDSL representation, ZX Caculus, or the generated circuit QASM.

Enjoy!
