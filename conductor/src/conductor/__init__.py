"""Conductor."""

from importlib.metadata import PackageNotFoundError, version  # type: ignore

from conductor.configs import get_config

try:
    __version__ = version(__name__)
except PackageNotFoundError:  # pragma: no cover
    __version__ = "unknown"

# Initialize global config
global_config = get_config()
