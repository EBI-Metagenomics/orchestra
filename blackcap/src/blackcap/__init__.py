"""Blackcap."""

from importlib.metadata import PackageNotFoundError, version  # type: ignore

# from blackcap import auther  # noqa: F401
from blackcap import blocs  # noqa: F401
from blackcap import cli  # noqa: F401
from blackcap import configs  # noqa: F401

# from blackcap import messenger  # noqa: F401
from blackcap import models  # noqa: F401
from blackcap import observer  # noqa: F401
from blackcap import routes  # noqa: F401

# from blackcap import scheduler  # noqa: F401
from blackcap import schemas  # noqa: F401

try:
    __version__ = version(__name__)
except PackageNotFoundError:  # pragma: no cover
    __version__ = "unknown"
