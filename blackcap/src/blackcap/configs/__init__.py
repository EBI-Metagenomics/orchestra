"""Blackcap configs."""

from blackcap.configs.default import DefaultConfig
from blackcap.configs.registry import ConfigRegistry
from blackcap.configs.testing import TestingConfig

config_registry = ConfigRegistry()
config_registry.add_config(DefaultConfig())
config_registry.add_config(TestingConfig())
