"""Random Scheduler implementation of Scheduler."""


from typing import List

from conductor.observer.base import BaseObserver
from conductor.schemas.metrics import Metrics


class ElasticObserver(BaseObserver):
    """Elastic observer to fetch metrics from Elastic stack."""

    def get_metrics(self: "BaseObserver", range: str) -> List[Metrics]:
        """Get cluster metrics.

        Args:
            range (str): time range

        Returns:
            List[Metrics]: List of metrics from each cluster # noqa: DAR202
        """
        return []
