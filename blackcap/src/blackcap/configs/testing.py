"""Testing blackcap config."""

from xdg import xdg_data_home

from blackcap.configs.default import DefaultConfig


class TestingConfig(DefaultConfig):
    """Testing config."""

    DB_NAME: str = "blackcap_test"
    DB_URI: str = f"sqlite:////{xdg_data_home() / ('orchestra') / ('blackcap_test.db')}"

    def get_config_name(self: "TestingConfig") -> str:
        """Return Config name.

        Returns:
            str: Name of the config
        """
        return "TESTING"
