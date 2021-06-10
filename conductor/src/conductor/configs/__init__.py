"""Conductor configs."""
from enum import Enum, unique
from functools import lru_cache

from conductor.configs.base import BaseConfig
from conductor.configs.default import DefaultConfig


@unique
class Config(Enum):
    """Config enum."""

    DEFAULT = DefaultConfig


@lru_cache()
def get_config(config: Config = Config.DEFAULT) -> BaseConfig:
    """Cache and return config object.

    Args:
        config (Config): Config to load

    Returns:
        BaseConfig: An instance of a class that inherits BaseConfig
    """
    return config.value()
