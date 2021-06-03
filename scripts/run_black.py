#! /bin/python3

from pathlib import Path
from subprocess import call

conductor_path = Path(__file__).parents[1].joinpath("conductor")
demon_path = Path(__file__).parents[1].joinpath("demon")

# Run black on conductor source
call(["poetry", "run", "black"], cwd=conductor_path)

# Run black on demon source
call(["poetry", "run", "black"], cwd=demon_path)
