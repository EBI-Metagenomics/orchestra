"""Base Scheduler class."""

from abc import ABC, abstractclassmethod
from typing import Dict

from conductor.schemas.job import Job


class BaseScheduler(ABC):
    """Base Scheduler class."""

    @abstractclassmethod
    def schedule(self: "BaseScheduler", job: Job, metrics: str) -> Dict:  # noqa: E501
        """Schedule a job.

        Args:
            job (Job): Job to schedule
            metrics (str): Current metrics from clusters

        Returns:
            Dict: Job Schedule # noqa: DAR202
        """
        pass
