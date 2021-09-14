"""Auther registry."""

from typing import Optional

from blackcap.auther.base import BaseAuther


class AutherRegistry:
    """Auther registry."""

    authers = {}

    def add_auther(self: "AutherRegistry", auther: BaseAuther) -> None:
        """Add custom authers to registry.

        Args:
            auther (BaseAuther): Custom auther implementation
        """
        self.authers[auther.CONFIG_KEY_VAL] = auther

    def get_auther(
        self: "AutherRegistry", auther: str
    ) -> Optional[BaseAuther]:  # noqa: E501
        """Get auther.

        Args:
            auther (str): Auther name

        Returns:
            Optional[BaseAuther]: Returns the auther if found else None
        """
        return self.authers.get(auther)
