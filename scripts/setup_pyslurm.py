#! /bin/python3
# flake8: noqa: S607, S603

"Setup PySlurm."

import shutil
from os import makedirs
from pathlib import Path
from subprocess import call

from urllib3 import PoolManager
from urllib3.exceptions import HTTPError


def download_file(url: str, path: Path) -> None:
    """Download and save file.

    Args:
        url (str): url of the file to download
        path (Path): path(including file name) to save downloaded file
    """
    pool = PoolManager()

    with open(path, "wb") as out:
        try:
            response = pool.request("GET", url, preload_content=False)
            shutil.copyfileobj(response, out)
        except HTTPError as e:
            print(e)
        response.release_conn()


conductor_path = Path(__file__).parents[1].joinpath("conductor")
demon_path = Path(__file__).parents[1].joinpath("demon")

try:
    # Download slurm
    slurm_version = "20.02.7"

    makedirs(name=demon_path.joinpath("external/build").absolute, exist_ok=True)

    download_file(
        url=f"https://download.schedmd.com/slurm/slurm-{slurm_version}.tar.bz2",
        path=demon_path.joinpath(f"external/slurm-{slurm_version}.tar.bz2").absolute,
    )

    # extract slurm files
    shutil.unpack_archive(
        demon_path.joinpath(f"external/slurm-{slurm_version}.tar.bz2")
    )

    # configure, make and install slurm

    call(
        ["configure", f"--prefix={demon_path.joinpath('external/build').absolute}"],
        cwd=demon_path.joinpath(f"external/slurm-{slurm_version}"),
    )

    call(
        ["make"],
        cwd=demon_path.joinpath(f"external/slurm-{slurm_version}"),
    )

    call(
        ["make", "install"],
        cwd=demon_path.joinpath(f"external/slurm-{slurm_version}"),
    )

    # Download pyslurm

    pyslurm_version = "20.02.0"

    download_file(
        url=f"https://github.com/PySlurm/pyslurm/archive/refs/tags/{pyslurm_version}.tar.gz",
        path=demon_path.joinpath(f"external/pyslurm-{pyslurm_version}.tar.gz").absolute,
    )

    # extract pyslurm files
    shutil.unpack_archive(
        demon_path.joinpath(f"external/pyslurm-{pyslurm_version}.tar.bz2")
    )

    # build pyslurm
    call(
        [
            "python",
            "setup.py",
            "build",
            f"--slurm-lib={demon_path.joinpath('external/build/lib').absolute}",
            f"--slurm-inc={demon_path.joinpath('external/build/include').absolute}",
        ],
        cwd=demon_path.joinpath(f"external/pyslurm-{pyslurm_version}"),
    )

    # install pyslurm
    call(
        [
            "python",
            "setup.py",
            "install",
        ],
        cwd=demon_path.joinpath(f"external/pyslurm-{pyslurm_version}"),
    )
except Exception as e:
    print(e)
