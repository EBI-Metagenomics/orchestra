"""Observer registry."""

from typing import Optional

from blackcap.observer.base import BaseObserver


class ObserverRegistry:
    """Observer registry."""

    observers = {}

    def add_observer(self: "ObserverRegistry", observer: BaseObserver) -> None:
        """Add custom observers to registry.

        Args:
            observer (BaseObserver): Custom observer implementation
        """
        self.observers[observer.CONFIG_KEY_VAL] = observer

    def get_observer(
        self: "ObserverRegistry", observer: str
    ) -> Optional[BaseObserver]:  # noqa: E501
        """Get observer.

        Args:
            observer (str): Observer name

        Returns:
            Optional[BaseObserver]: Returns the observer if found else None
        """
        return self.observers.get(observer)
