#! /bin/python3
"""Helper script to run flake8 in all python sub projects."""

from pathlib import Path
from subprocess import call

conductor_path = Path(__file__).parents[1].joinpath("conductor")
demon_path = Path(__file__).parents[1].joinpath("demon")

# Run flake8 on conductor source
call(["poetry", "run", "flake8"], cwd=conductor_path)

# Run flake8 on demon source
call(["poetry", "run", "flake8"], cwd=demon_path)
