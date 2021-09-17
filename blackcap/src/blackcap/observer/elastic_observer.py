"""Random Scheduler implementation of Scheduler."""


from typing import List

from blackcap.observer.base import BaseObserver
from blackcap.schemas.metrics import Metrics


class ElasticObserver(BaseObserver):
    """Elastic observer to fetch metrics from Elastic stack."""

    CONFIG_KEY_VAL = "ELASTIC"

    def get_metrics(self: "BaseObserver", range: str) -> List[Metrics]:
        """Get cluster metrics.

        Args:
            range (str): time range

        Returns:
            List[Metrics]: List of metrics from each cluster # noqa: DAR202
        """
        return []
