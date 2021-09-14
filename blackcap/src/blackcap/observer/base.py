"""Base Observer class."""

from abc import ABC, abstractclassmethod
from typing import List

from blackcap.schemas.metrics import Metrics


class BaseObserver(ABC):
    """Base Observer class."""

    @abstractclassmethod
    def get_metrics(self: "BaseObserver", range: str) -> List[Metrics]:  # noqa: E501
        """Get cluster metrics.

        Args:
            range (str): time range

        Returns:
            List[Metrics]: List of metrics from each cluster # noqa: DAR202
        """
        pass
