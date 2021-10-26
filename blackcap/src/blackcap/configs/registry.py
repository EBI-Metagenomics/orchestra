"""Config registry."""

from typing import Optional
import os

from blackcap.configs.base import BaseConfig, ConfigOfConfig


class ConfigRegistry:
    """Config registry."""

    configs = {}
    config_of_config = ConfigOfConfig()

    def add_config(self: "ConfigRegistry", config: BaseConfig) -> None:
        """Add custom configs to registry.

        Args:
            config (BaseConfig): Custom config implementation
        """
        self.configs[config.get_config_name()] = config

    def get_config(
        self: "ConfigRegistry", config: str = config_of_config.BLACKCAP_CONFIG
    ) -> Optional[BaseConfig]:  # noqa: E501
        """Get config.

        Args:
            config (str): Config name

        Returns:
            Optional[BaseConfig]: Returns the config if found else None
        """
        return self.configs.get(config)
