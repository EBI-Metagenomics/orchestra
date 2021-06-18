"""CLI commnad util functions."""


import subprocess  # noqa: S404
import sys
from typing import List, Optional, Union

from demon.configs import get_config
from demon.configs.base import BaseConfig

default_config = get_config()


def call_cli(
    cmd: List[str],
    input: Optional[str] = None,
    timeout: Optional[float] = None,
    config: BaseConfig = default_config,
) -> Union[str, bytes]:
    """Call CLI commands.

    Args:
        cmd (List[str]): [description]
        input (Optional[str]): [description]. Defaults to None.
        timeout (Optional[float]): [description]. Defaults to None.
        config (BaseConfig): [description]. Defaults to default_config.

    Returns:
        Union[str, bytes]: Stdout
    """
    proc = subprocess.Popen(  # noqa: S603
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8",
        errors="replace",
    )
    stdout, stderr = proc.communicate(input=input, timeout=timeout)
    sys.stderr.write(stderr)
    return stdout
