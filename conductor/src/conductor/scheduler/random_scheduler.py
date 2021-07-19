"""Random Scheduler implementation of Scheduler."""


from typing import Dict

from conductor.scheduler.base import BaseScheduler
from conductor.schemas.job import Job


class RandomScheduler(BaseScheduler):
    """Random scheduler schedule jobs randomly."""

    def schedule(self: "RandomScheduler", job: Job, metrics: str) -> Dict:
        """Schedule a job.

        Args:
            job (Job): Job to schedule
            metrics (str): Current metrics from clusters

        Returns:
            Dict: Job Schedule
        """
        return {}
