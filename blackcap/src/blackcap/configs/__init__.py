"""Blackcap configs."""
from enum import Enum, unique
from functools import lru_cache

from blackcap.configs.base import BaseConfig
from blackcap.configs.default import DefaultConfig


@unique
class ConfigEnum(Enum):
    """Config enum."""

    DEFAULT = DefaultConfig


@lru_cache()
def get_config(config: ConfigEnum = ConfigEnum.DEFAULT) -> BaseConfig:
    """Cache and return config object.

    Args:
        config (ConfigEnum): Config to load

    Returns:
        BaseConfig: An instance of a class that inherits BaseConfig
    """
    return config.value()
