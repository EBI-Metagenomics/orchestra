"""Blackcap configs."""
from enum import Enum, unique
from functools import lru_cache

from blackcap.configs.default import DefaultConfig
from blackcap.configs.registry import ConfigRegistry

config_registry = ConfigRegistry()
config_registry.add_config(DefaultConfig())
