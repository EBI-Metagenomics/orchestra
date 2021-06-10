#! /bin/python3
# flake8: noqa: S607, S603

"""Setup scripts."""

from pathlib import Path
from subprocess import call

from urllib3 import PoolManager
from urllib3.exceptions import HTTPError

conductor_path = Path(__file__).parents[1].joinpath("conductor")
demon_path = Path(__file__).parents[1].joinpath("demon")


try:
    # Install conductor deps
    call(["poetry", "install"], cwd=conductor_path)
    # Calling again as a workaround to ensure project root is installed
    call(["poetry", "install"], cwd=conductor_path)

    # Install demon deps
    call(["poetry", "install"], cwd=demon_path)
    # Calling again as a workaround to ensure project root is installed
    call(["poetry", "install"], cwd=demon_path)

except Exception as e:
    print(e)
