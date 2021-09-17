"""Messenger registry."""

from typing import Optional

from blackcap.messenger.base import BaseMessenger


class MessengerRegistry:
    """Messenger registry."""

    messengers = {}

    def add_messenger(self: "MessengerRegistry", messenger: BaseMessenger) -> None:
        """Add custom messengers to registry.

        Args:
            messenger (BaseMessenger): Custom messenger implementation
        """
        self.messengers[messenger.CONFIG_KEY_VAL] = messenger

    def get_messenger(
        self: "MessengerRegistry", messenger: str
    ) -> Optional[BaseMessenger]:  # noqa: E501
        """Get messenger.

        Args:
            messenger (str): Messenger name

        Returns:
            Optional[BaseMessenger]: Returns the messenger if found else None
        """
        return self.messengers.get(messenger)
