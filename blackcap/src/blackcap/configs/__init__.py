"""Blackcap configs."""

from blackcap.configs.default import DefaultConfig
from blackcap.configs.registry import ConfigRegistry

config_registry = ConfigRegistry()
config_registry.add_config(DefaultConfig())
