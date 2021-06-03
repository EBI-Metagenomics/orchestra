#! /bin/python3

from pathlib import Path
from subprocess import call

conductor_path = Path(__file__).parents[1].joinpath("conductor")
demon_path = Path(__file__).parents[1].joinpath("demon")

# Install conductor deps
call(["poetry", "install"], cwd=conductor_path)

# Install demon deps
call(["poetry", "install"], cwd=demon_path)
